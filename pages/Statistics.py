import streamlit as st
from firebase_admin import firestore
db = firestore.client()
from utils import sidebar

st.set_page_config(page_title="Statistiques")

"""n livres les plus empruntés"""
def get_most_borrowed_books(n=5):
    all_borrows = db.collection("emprunt").stream()
    borrow_count = {}

    for borrow in all_borrows:
    book_title = borrow.to_dict().get("book_title")
    if book_title in borrow_count:
        borrow_count[book_title] += 1
    else:
    borrow_count[book_title] = 1

sorted_books = sorted(borrow_count.items(), key=lambda x: x[1], reverse=True)
return sorted_books[:n]

"""n utilisateurs avec le plus d'emprunts"""
def get_top_users(n=5):
    all_borrows = db.collection("emprunts").stream()
    user_count = {}

    for borrow in all_borrows:
        user_email = borrow.to_dict().get("user_email")
        if user_email in user_count:
            user_count[user_email] += 1
        else:
            user_count[user_email] = 1

    sorted_users = sorted(user_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_users[:n]

"""Pourcentage de retours en retard"""
def get_late_returns():
    all_borrows = db.collection("emprunts").stream()
    total_borrows = 0
    late_returns = 0

    for borrow in all_borrows:
        total_borrows += 1
        due_date = borrow.to_dict().get("due_date")
        if datetime.now() > due_date:
            late_returns += 1

    return (late_returns / total_borrows * 100) if total_borrows > 0 else 0

def run():
    st.title("Statistiques de la Bibliothèque")

    st.subheader("Livres les Plus Empruntés")
    most_borrowed_books = get_most_borrowed_books()
    for title, count in most_borrowed_books:
        st.write(f"{title}: {count} emprunts")

    st.subheader("Utilisateurs avec le Plus d'Emprunts")
    top_users = get_top_users()
    for email, count in top_users:
        st.write(f"{email}: {count} emprunts")

    st.subheader("Pourcentage de Retours en Retard")
    late_return_percentage = get_late_returns()
    st.write(f"{late_return_percentage:.2f}% des retours sont en retard.")

        
run()
