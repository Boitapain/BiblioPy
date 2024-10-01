import streamlit as st
from firestore_utils import add_book_to_firestore
from utils import sidebar

st.set_page_config(page_title="Ajouter un livre")
def run():
    sidebar()
    st.title("Ajouter un Livre")
    title = st.text_input("Titre du livre")
    author = st.text_input("Auteur du livre")
    isbn = st.text_input("ISBN")
    available_copies = st.number_input("Nombre de copies disponibles", min_value=1, step=1)
    
    if st.button("Ajouter livre"):
        add_book_to_firestore(title, author, isbn, available_copies)

run()