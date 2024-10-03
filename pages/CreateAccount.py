import streamlit as st
from firestore_utils import add_user_to_firestore
from utils import set_user_info

st.set_page_config(page_title="Créer un compte")

def run():
    st.title("Créer un compte")
    new_name = st.text_input("Nom d'utilisateur")
    new_email = st.text_input("Votre email")

    if st.button("Créer un compte"):
        add_user_to_firestore(new_name, new_email)
        set_user_info(new_name, new_email)
        st.rerun()
        st.rerun()
run()