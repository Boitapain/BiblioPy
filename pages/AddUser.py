import streamlit as st
from firestore_utils import add_user_to_firestore
from utils import sidebar

st.set_page_config(page_title="Ajouter un utilisateur")
def run():
    sidebar()
    st.title("Ajouter un utilisateur")
    name = st.text_input("Nom de l'utilisateur")
    email = st.text_input("Email de l'utilisateur")

    if st.button("Ajouter utilisateur"):
        add_user_to_firestore(name, email)

run()