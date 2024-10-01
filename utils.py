import streamlit as st

def sidebar():
    st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
    st.sidebar.page_link("pages/AddBook.py", label="Ajouter un livre", icon="📕")
    st.sidebar.page_link("pages/AddUser.py", label="Ajouter un utilisateur", icon="👤")
    st.sidebar.page_link("pages/BorrowBook.py", label="Emprunter un livre", icon="📚")
    st.sidebar.page_link("pages/ReturnBook.py", label="Rendre un livre", icon="📥")
    st.sidebar.page_link("pages/Statistics.py", label="Statistiques", icon="📊")