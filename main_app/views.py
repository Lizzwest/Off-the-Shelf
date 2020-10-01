from django.shortcuts import render
from .models import Comment, Wishlist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests, xmltodict, json
# from decouple import config
import os
from django.core.paginator import Paginator



######################### Index #########################

def index(request):    
    return render(request, 'index.html')

######################### Login #########################

def login_view(request):
    if request.method =="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+str(user))
                else:print('The account has been disable YOU SCOUNDREL')
        else:
            print('The username and/or password is incorrect. You are less of a scoundrel')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})

######################### Logout #########################

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

######################### Signup #########################

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else: 
            return HttpResponse('<h1>Try Again</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

######################### Profile #########################   
     
@login_required
def profile(request, username):
    if request.method == "POST":
        delete_comment = request.POST.get("delete_comment")
        if delete_comment:
            Comment.objects.filter(id=delete_comment).delete()
        else:
            delete = request.POST.get("delete")
            if delete:
                Wishlist.objects.filter(book_id=delete).delete()
            else:
                title = request.POST.get("title")
                id = request.POST.get("id")
                img_url = request.POST.get("image")
                user = request.user 

                exist = Wishlist.objects.filter(book_id=id)
                if exist:
                    pass
                else:
                    Wishlist.objects.create(
                        title = title,
                        book_id = id,
                        img_url = img_url,
                        user = user
                    )
    user = User.objects.get(username=username)
    wishlists = Wishlist.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'wishlists': wishlists, "comments": comments})

######################### Search Result #########################

def search_results(request):
    if request.method == 'POST':
        search = request.POST.get("search")

        response = requests.get('https://www.goodreads.com/search.xml?key={}&q={}'.format(os.environ('key'), search))
    
        data = xmltodict.parse(response.content)
        jsonData = json.dumps(data)
        theData = json.loads(jsonData)
        searchList = theData["GoodreadsResponse"]["search"]["results"]["work"]

        booklist = []
        # check number of search results, if more than 10 return first 10
        num_results = len(searchList)
        if num_results > 10: 
            num_results = 10

        for i in range(num_results):
            book = {
                "title": searchList[i]["best_book"]["title"],
                "author": searchList[i]["best_book"]["author"]["name"],
                "img_url": searchList[i]["best_book"]["image_url"],
                "average_rating": searchList[i]["average_rating"],
                "id": searchList[i]["best_book"]["id"]['#text'],
            }
    
            booklist.append(book)
        # return(booklist)
    # paginator = Paginator(booklist, 2)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    return render(request, 'search_results.html', {"booklist": booklist} )

######################### Book Show #########################

def book_show(request, id):
    # method to add a new comment
    if request.method == 'POST':
        content = request.POST.get("content")
        id = request.POST.get("id")
        user = request.user
        title = request.POST.get("title")

        Comment.objects.create(
            content=content,
            book_id = id,
            user = user,
            title = title,
        )

    # get existing comments about this book from our database
    comments = Comment.objects.filter(book_id=id)
    # get book details from goodreads api
    response = requests.get('https://www.goodreads.com/book/show/{}.xml?key={}'.format(id, os.environ('key')))
    data = xmltodict.parse(response.content)
    jsonData = json.dumps(data)
    theData = json.loads(jsonData)
    book = theData["GoodreadsResponse"]["book"]
    similar = []
    buyLinks = []
    
    # helper function to cleanup book description
    def clean_text(txt):
        unwanted_tags = ['<br />', '<b>', '</b>', '<i>', '</i>', '<em>', '</em>', '<a>', '</a>', '<p>', '</p>']
        for i in unwanted_tags:
            if i in txt:
                txt = ''.join(txt.split(i))
        return(txt)

    # check if book description exist
    description = book["description"]
    if description: # clean description if it exits
        description = clean_text(book["description"])
    else:
        description = ''
    
    # check if author is a dictionary
    # TODO handle multiple authors
    author_type = type(book["authors"]["author"])
    if author_type is dict:
        author = book["authors"]["author"]["name"]
        author_link = book["authors"]["author"]["link"]
    else:
        author = book["authors"]["author"][0]["name"]
        author_link = book["authors"]["author"][0]["link"]

    # store details of the book into a dictionary
    detail = {
        "title": book["title"],
        "author": author,
        "author_link": author_link,
        "description": description,
        "img_url": book["image_url"],
        "average_rating": book["average_rating"],
        "id": book["id"],
        "isbn": book["isbn"]
    }

    # helper function to get rid of () in book title if it's in a series
    def clean_title(txt):
        if '(' in txt:
            txt = txt.split('(')
            return(txt[0])
        else:
            return(txt)

    # search movie from omdb api by this book title
    title = clean_title(detail["title"])
    omdb_response = requests.get('http://www.omdbapi.com/?t={}&apikey={}'.format(title, os.environ('omdb_key')))
    movie_data = json.loads(omdb_response.content)
    # check if the writer of the movie is the same of the book author 
    if "Title" in movie_data:
        if "Writer" in movie_data:
            if detail["author"] in movie_data["Writer"] or detail["author"] in movie_data["Plot"] or movie_data["Writer"] == 'N/A':            
                movie = {
                    "title": movie_data["Title"],
                    "year": movie_data["Year"],
                    "director": movie_data["Director"],
                    "writer": movie_data["Writer"],
                    "poster": movie_data["Poster"],
                    "imdbRating": movie_data["imdbRating"],
                    "plot": movie_data["Plot"]
                }
            else: 
                movie = {
                    "None": "No movie based on this book yet."
                }
        else:
            movie = {
                "None": "No movie based on this book yet."
            }
    else:
        movie = {
            "None": "No movie based on this book yet."
        }
    
    # get 6 similar books stored in a dictionary
    if "similar_books" in book:
        num_books = len(book["similar_books"]["book"])
        if num_books > 6:
            num_books = 6
        for i in range(num_books):
            similar_books = {
                "id": book["similar_books"]["book"][i]["id"],
                "title" : book["similar_books"]["book"][i]["title"],
                "image_url": book["similar_books"]["book"][i]["image_url"]
            }
            similar.append(similar_books)
    else:
        similar.append({"None": "Cannot find similar books."})

    # return stored dictionaries
    return render(request, 'book_show.html', {
        "detail": detail,
        "similar": similar,
        "buyLinks": buyLinks,
        "comments":comments,
        "did": os.environ('key'),
        "movie": movie
    })
    
class CommentUpdate(UpdateView):
    model = Comment
    fields = ['content']
    def form_valid(self, form): 
        self.object = form.save(commit=False) 
        self.object.save()
        user = self.object.user.username
        return HttpResponseRedirect('/user/' + user)

def handler404(request):
    return render(request, '404.html', status=404)
# def handler500(request):
#     return render(request, '500.html', status=500)

