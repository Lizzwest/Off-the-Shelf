# Off-The-Shelf
This is our Final Project for General Assembly. Off the Shelf is a one stop shop for all things books. You can search by title or by author. Once you've selected a book, you are able to see additional information, such as similar books, ratings and reviews, buy links to purchase the book and information on any film or tv adaptations of the book. You can also save books to check out later to your Wishlist.

### Deployed Link
offtheshelff.herokuapp.com

## Tech Stack
Django
PostgresQL

## Added Tech
- GoodReads API
- OMDB API
- 

### Pip installations
- requests
- xmljson
- xmltodict
- python decouple
- django-crispy-forms
- psycopg2
- gunicorn

We also installed add on's for heroku to deploy online.


## Instructions to install

- Fork and clone this repo. 
- Open this application in your code editor ( we used VS code).
- *```Touch```* a ```.env``` . The ```.env``` file will require a ```SECRET_KEY```for your session, an ```omdb_key``` for the OMDB API,  and a ```KEY``` from GoodReads API.
- Run ```python3 manage.py runserver```  to open and start the application in your browser.
## User Stories

- As a User, I want to be able to create and delete an account.
- As a User, I want to be able to search for books by title or author.
- As a User, I want to be able to click a link to purchase a book.
- As a User, I want to be able to see added details about the book, such as similar books, ratings and reviews, and whether or not the book has been converted to TV/Film.
- As a User, I want to be able to comment on a book, and delete my comment if I change my mind.
- As a User, I want to be able to save books that I want to read/ buy to a wishlist.

## Models

### User Model

| Column Name | Data Type | Notes |
| --------------- | ------------- | ------------------------------ |
| id | Integer | Serial Primary Key, Auto-generated |
| username | CharField | Must be provided; used for login |
| password | CharField | Stored as a hash |
| password2 | CharField | Stored as a hash; must match password |


### Comment Model
| Column Name | Data Type | Notes |
| --------------- | ------------- | ------------------------------ |
| id | Integer | Serial Primary Key, Auto-generated |
| content |  | Must be provided |
| book_id | CharField | Provided by API|
| title | CharField | Provided by API |
| user | ForeignKey | Auto-generated from User Model|

### Wishlist Model
| Column Name | Data Type | Notes |
| --------------- | ------------- | ------------------------------ |
| id | Integer | Serial Primary Key, Auto-generated |
| img_url | CharField | Provided by API|
| book_id | CharField | Provided by API|
| title | CharField | Provided by API |
| user | ForeignKey | Auto-generated from User Model|



## Wireframes/ERD
![erd](offtheshelf/main_app/static/assets/erd.png)
![wireframe](offtheshelf/main_app/static/assets/wireframe1.png)
![wireframe](offtheshelf/main_app/static/assets/wireframe2.png)
![wireframe](offtheshelf/main_app/static/assets/wireframe3.png)
![wireframe](offtheshelf/main_app/static/assets/wireframe4.png)

## The Dev Team

- Margaret Huang 
- Nick Phillips
- Steven Michaud
- Lizz West


### The Struggles 

- Steven
    - A struggle for me would be hiding the api keys, and using imdbpy. It did not return the all the data I wanted, so going with the ombd was a better solution. Also, writing the function to compare the book title with the movie title as well as comparing the book author with the correct writer of the movie.
- Margaret
    - The big struggle with the API also ended up being my victory, so I will address it below.
- Nick
    - My struggle was also my victory, which was implementing the audio file. It was hard because we wanted it to auto loop, but we also didn't want the audio controls displaying standard.
- Lizz
    - It was difficult to get all HTML's rendering properly, especially with django's built in debug feature. Took about 2 days of going back and forth to finally get everything rendering as intended.



### The Victories

- Steven 
    - A victory for me was finding python-decouple for hiding sensitive data, like api-keys. Also, finding that the omdb api contains the book author under writers for cross referencing to the book.
- Margaret
    - The GoodReads API returns data in xml format, so  we had to import the ```requests``` and ```xmltodict``` modules from python to convert it into ```json``` format. And we dig into the data to find what we need for our site.
- Nick
    - Finally getting the audio track working and having it play at the user's request. It is also an original audio track I composed and mastered for this project.
- Lizz
    - My biggest victory was the styling all coming together and learning how to customize icons for a site, giving it a more user-friendly feel.

### What comes next

- We want to continue to play with the API's we included to see if there are any additional features we can add in, such as a Movie show page for all details on film adaptations.
- We would also like to implement a resell page for used books. Giving people a chance to share their books with someone who maybe cannot afford to purchase one at full price, or a book that is harder to come by.