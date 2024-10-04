import streamlit as st

def sidebar():
    st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
    st.sidebar.page_link("pages/AddBook.py", label="Ajouter un livre", icon="📕")
    st.sidebar.page_link("pages/BorrowBook.py", label="Emprunter un livre", icon="📚")
    st.sidebar.page_link("pages/ReturnBook.py", label="Rendre un livre", icon="📥")
    st.sidebar.page_link("pages/Statistics.py", label="Statistiques", icon="📊")
    if st.sidebar.button("↪️ Déconnexion"):
        logout()

def logout():
    st.session_state.clear()
    st.session_state.redirected_from_logout = True  
    st.rerun()

def set_user_info(name, email):
    if name and email: 
        st.session_state.username = name
        st.session_state.email = email
    else:
        st.warning("Nom ou email manquant. Veuillez entrer les deux.")

def get_user_info():
    if 'username' in st.session_state and 'email' in st.session_state:
        return {
            "username": st.session_state.username,
            "email": st.session_state.email
        }
    else:
        return None