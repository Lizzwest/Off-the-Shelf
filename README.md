# Off-The-Shelf
This is our Final Project for General Assembly. Off the Shelf is a one stop shop for all things books. You can search by title or by author. Once you've selected a book, you are able to see additional information, such as similar books, ratings and reviews, buy links to purchase the book and information on any film or tv adaptations of the book. You can also save books to check out later to your Wishlist.




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
- 


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





