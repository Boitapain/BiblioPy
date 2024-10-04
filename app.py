import streamlit as st
from firebase_admin import firestore
from firebase_utils import initialize_firebase
initialize_firebase()

from utils import sidebar
db = firestore.client()
from utils import get_user_info
from pages import Login, CreateAccount

def display():
    st.title("BiblioPy - Accueil")
    st.subheader("Bienvenue à BiblioPy")
    sidebar()
    books_ref = db.collection("books").stream()

    st.write("---")
    
    # Custom CSS for the book display
    st.markdown("""
        <style>
        .book-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #E3EED9;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 15px;
            height: 100px; /* Ensures consistent height */
        }
        .book-title, .book-author, .book-isbn, .book-available {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 1;
            text-align: center;
        }
        .book-title {
            font-weight: bold;
        }
        .book-author {
            font-style: italic;
            font-weight: bold;
        }
        .book-isbn {
            font-weight: 900;
        }
        .book-available {
            font-weight: normal;
        }
        .custom-button {
            background-color: #FFFFFF;
            border: none;
            border-radius: 5px;
            margin-left: 8px;
            padding: 4px 8px;  /* Smaller padding */
            cursor: pointer;
            font-size: 14px;  /* Smaller font size */
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .custom-button:hover {
            background-color: #ddd;  
        }
        </style>
    """, unsafe_allow_html=True)

    for book in books_ref:
        book_data = book.to_dict()
        
        # HTML layout for each book with custom styles
        st.markdown(f"""
        <div class="book-container">
            <div class="book-title">{book_data['title']}</div>
            <div class="book-author">{book_data['author']}</div>
            <div class="book-isbn">{book_data['isbn']}</div>
            <div class="book-available">{book_data['available_copies']} copies disponibles</div>
            <button class="custom-button" onclick="editBook('{book.id}')">✏️</button>
            <button class="custom-button" onclick="deleteBook('{book.id}')">🗑️</button>
        </div>
        """, unsafe_allow_html=True)
        
def editBook():
    return None
            
def run():
    user_info = get_user_info()
    
    if "create_account_clicked" not in st.session_state:
        st.session_state.create_account_clicked = False

    if "login_clicked" not in st.session_state:
        st.session_state.login_clicked = False
    
    if user_info is None:
        st.subheader("Choisissez une option de connexion")
        
        if st.button("Créer un nouveau compte"):
            st.session_state.create_account_clicked = True
            st.session_state.login_clicked = False

        if st.button("Se connecter"):
            st.session_state.login_clicked = True
            st.session_state.create_account_clicked = False

        if st.session_state.create_account_clicked:
            CreateAccount.run()

        if st.session_state.login_clicked:
            Login.run()
    else:
        display()
run()