import streamlit as st
from firestore_utils import get_all_users, get_all_borrowable_books, get_user_by_email, get_book_by_title, add_borrow_record, MAX_BORROW_LIMIT
from datetime import datetime
from dateutil.relativedelta import relativedelta
from firebase_admin import firestore
db = firestore.client()
from utils import sidebar

st.set_page_config(page_title="Emprunter un livre")

def is_book_reserved_by_user(user_email, book_title):
    #Vérifie si l'utilisateur a déjà réservé ce livre.
    reservations = db.collection("reservations").where("user_email", "==", user_email).where("book_title", "==", book_title).stream()
    return len(list(reservations)) > 0


def run():
    sidebar()
    st.title("Emprunter un livre")
    users = get_all_users()
    books = get_all_borrowable_books()
    
    user_email = st.selectbox("Email de l'utilisateur", options=[user["email"] for user in users])
    book_title = st.selectbox("Titre du livre", options=[book["title"] for book in books])

    if st.button("Emprunter"):
        user = get_user_by_email(user_email)
        book = get_book_by_title(book_title)

        if user and book:
            if "borrowed_books" not in user:
                user["borrowed_books"] = []
                
            if len(user["borrowed_books"]) >= MAX_BORROW_LIMIT:
                st.error(f"L'utilisateur a atteint la limite de {MAX_BORROW_LIMIT} prêts.")
            elif book["available_copies"] < 1:
                st.warning("Livre non disponible. Réservation automatique.")
                db.collection("reservations").add({
                    "user_email": user_email,
                    "book_title": book_title,
                    "reserved_at": datetime.now()
                })
                st.success("Réservation effectuée.")
            else:
                borrowed_at = datetime.now()
                due_date = datetime.now() + relativedelta(weeks=2)

                add_borrow_record(user_email, book_title, borrowed_at, due_date)
                
                user["borrowed_books"].append({"book_title": book_title, "due_date": due_date})
                db.collection("users").document(user["id"]).update({"borrowed_books": user["borrowed_books"]})

                book["available_copies"] -= 1
                db.collection("books").document(book["id"]).update({"available_copies": book["available_copies"]})
                
                st.success(f"Le livre '{book_title}' a été emprunté avec succès par {user_email}. Retour prévu le {due_date.strftime('%d-%m-%Y')}")
        else:
            st.warning("Le mail ou le livre n'existe pas")
run()
