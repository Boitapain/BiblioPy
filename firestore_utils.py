from firebase_utils import get_firestore_client

db = get_firestore_client()

MAX_BORROW_LIMIT = 3

# Function to add a book to Firestore
def add_book_to_firestore(title, author, isbn, available_copies):
    book_data = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "available_copies": available_copies,
        "borrowed_by": []
    }
    db.collection("books").add(book_data)

# Function to add a user to Firestore
def add_user_to_firestore(name, email):
    user_data = {
        "name": name,
        "email": email,
        "borrowed_books": [],
        "fines": 0
    }
    db.collection("users").add(user_data)

# Function to get a user by email
def get_user_by_email(email):
    user_ref = db.collection("users").where("email", "==", email).stream()
    user = None
    for u in user_ref:
        user = u.to_dict()
        user["id"] = u.id
    return user

# Function to get all users
def get_all_users():
    users_ref = db.collection("users").stream()
    return [user.to_dict() for user in users_ref]

# Function to get a book by title
def get_book_by_title(title):
    books_ref = db.collection("books").where("title", "==", title).stream()
    book = None
    for b in books_ref:
        book = b.to_dict()
        book["id"] = b.id
    return book

# Function to get all borrowable books
def get_all_borrowable_books():
    books_ref = db.collection("books").where("available_copies", ">", 0).stream()
    return [book.to_dict() for book in books_ref]

# Function to get all borrowed books of a user
def get_all_borrowed_books(user_email):
    user = get_user_by_email(user_email)
    if user:
        return user["borrowed_books"]
    return []
