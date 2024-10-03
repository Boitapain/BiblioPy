import streamlit as st
from firebase_admin import firestore
from firebase_utils import initialize_firebase
initialize_firebase()

from utils import sidebar
db = firestore.client()
from utils import get_user_info
from pages import Login

def display():
    st.title("BiblioPy - Accueil")
    st.subheader("Bienvenue à BiblioPy")
    sidebar()
    books_ref = db.collection("books").stream()
    st.write(get_user_info())

    st.write("---")
    for book in books_ref:
        book_data = book.to_dict()
        cols = st.columns(4)

        with cols[0]:
            st.write(f"**Titre:** {book_data['title']}")
        with cols[1]:
            st.write(f"**Auteur:** {book_data['author']}")
        with cols[2]:
            st.write(f"**ISBN:** {book_data['isbn']}")
        with cols[3]:
            st.write(f"**Copies disponibles:** {book_data['available_copies']}")

        st.write("---")

def run():
    user_info = get_user_info()
    if user_info is None:
        Login.run()
    else:
        display()
run()