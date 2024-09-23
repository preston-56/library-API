# Library Management System (Django RESTful API)
### Overview
- This project is a Django-based RESTful API designed to manage books and authors, with a focus on user authentication, search functionality, and book recommendation. 
- The system supports adding, updating, retrieving, and deleting books and authors, while also providing a recommendation system based on user favorites.
---

### Key Features:
1. **User Authentication**: JWT-based authentication for secure API access.
2. **CRUD Operations**:  Create, retrieve, update, and delete books and authors.
3. **Search Functionality**: Search for books by title or author name.
4. **Recommendation System**: Suggest similar books based on a user’s favorites list.
   
---

### API Endpoints
#### **Books**:
- `GET /books`: Retrieve a list of all books.
- `GET /books/:id`: Retrieve a specific book by ID.
- `POST /books`: Create a new book (JWT Protected).
- `PUT /books/:id`: Update an existing book (JWT Protected).
`DELETE /books/:id`: Delete a book (JWT Protected).

### **Authors**:
- `GET /authors`: Retrieve a list of all authors.
- `GET /authors/:id`: Retrieve a specific author by ID.
- `POST /authors`: Create a new author (JWT Protected).
- `PUT /authors/:id`: Update an existing author (JWT Protected).
- `DELETE /authors/:id`: Delete an author (JWT Protected).

### **User Authentication**:
- `POST /register`: User registration endpoint.
- `POST /login`: User login, returns JWT tokens.

### **Search Functionality**:
- `GET /books?search=query`: Search for books by title or author name.


### **Favorites and Recommendations**:
- `POST /favorites`: Add a book to the user's favorites list (JWT Protected).
- `DELETE /favorites/:id`: Remove a book from the user's favorites list (JWT Protected).
- `GET /favorites/`: Get 5 recommended books based on the user’s favorite books ==(JWT Protected).
---
### **Database Schema**
##### Models
- **User**: The built-in Django `User` model is extended to support user registration and authentication via JWT.
- **Book**:
```python

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
```
- **Author**:
``` python
class Author(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(blank=True)
    bio = models.TextField(blank=True) 
```
- **Favorite**:
```python
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
```
### **Relationships**:
- **Book-Author**: A `Book` is linked to an `Author` through a Foreign Key.
- **User-FavoriteBook**: A user can have multiple favorite books, stored in the `Favorite` model, which links a `User` and a `Book`.
- ---
### Recommendation System
- The recommendation system is designed to suggest books similar to those marked as favorites by the user. A similarity algorithm is employed to recommend books based on matching authors, genres, or other factors.
- **Recommendation Endpoint**: `GET /favorites/recommendations` provides up to 5 similar books based on a user’s favorite books, calculated in less than 1 second.
  
### **Algorithm**:
- A basic similarity algorithm based on matching authors, genres, and keywords. The system compares the user’s favorite books to the entire dataset and recommends titles with the highest similarity score.
- #### Logic:
  - Find books by the same author.
  - Find books in the same genre (if applicable).
  - Use cosine similarity or another similarity metric on book descriptions or keywords.
  - ---

### Search Functionality
- **Endpoint**: `GET /books?search=query`
- The search functionality allows users to search books by title or author name.
- It supports partial matches and is case-insensitive.
### Security
- JWT is used for user authentication.
- Protected endpoints (create, update, delete books/authors) require a valid JWT token.
- Only registered users can access the recommendation and favorites functionality.

### Performance
- The recommendation system is designed to return results within 1 second, even for large datasets.
- **Optimization Strategies**:
   - Efficient database queries with indexing.
   - Caching frequently requested data.
   - Using Django’s `select_related` and `prefetch_related` to minimize database hits.

### Setting Up the Project
1. Clone the Repository
   ```bash
   git clone git@github.com:preston-56/library-API.git
   cd library-API
   ```

2. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Setup the Database
   ```bash
   python3 manage.py migrate
   ```
4. Run the Server
   ```bash
   python3 manage.py runserver
   ```
5. Register a New User and Login
   - Use `/register` to create a new user.
   - Use `/login` to generate a JWT token for authentication.
  
Once logged in, use the provided endpoints to manage books and authors.

---
