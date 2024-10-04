import streamlit as st
from firestore_utils import get_user_by_email
from utils import set_user_info, get_user_info

def run():
    st.title("Se connecter")
    email = st.text_input("Email")
    if st.button("Connexion"):
        user = get_user_by_email(email)
        if user :
            set_user_info(user["name"], user["email"])
            st.rerun()
            st.rerun()
        else : 
            st.warning("L'email n'existe pas")

run()