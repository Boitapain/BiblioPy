import streamlit as st
from firebase_admin import firestore
from utils import sidebar
db = firestore.client()

st.set_page_config(page_title="Accueil")


def run():
    st.title("BiblioPy - Accueil")
    st.subheader("Bienvenue à BiblioPy")
    sidebar()
    books_ref = db.collection("books").stream()

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
run()