import streamlit as st
from firebase_admin import firestore
db = firestore.client()
from utils import sidebar

st.set_page_config(page_title="Statistiques")

def run():
    sidebar()
    st.title("Statistiques")
    books_ref = db.collection("books").stream()
    for book in books_ref:
        book_data = book.to_dict()
        st.write(f"{book_data['title']}: {len(book_data['borrowed_by'])} emprunts")
        
run()
