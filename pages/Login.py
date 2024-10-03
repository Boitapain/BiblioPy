import streamlit as st
from firestore_utils import get_user_by_email
from utils import set_user_info, get_user_info
from pages import AddUser

def run():
    st.title("Connectez Vous")
    email = st.text_input("Email")
    if st.button("Se connecter"):
        st.warning(email)
        user = get_user_by_email(email)
        if user :
            set_user_info(user["name"], user["email"])
        else : 
            st.warning(get_user_info())
            st.warning("L'email n'existe pas")
    if st.button("Créer un nouveau compte"):
        AddUser.run()
        st.rerun()
run()