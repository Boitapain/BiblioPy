import streamlit as st
from firestore_utils import get_all_users, get_all_borrowed_books, get_user_by_email, get_book_by_title, MAX_BORROW_LIMIT
from datetime import datetime, timezone
from firebase_admin import firestore
db = firestore.client()
from utils import sidebar

st.set_page_config(page_title="Retourner un livre")

def run():
    sidebar()
    st.title("Retourner un livre")
    users = get_all_users()
    user_email = st.selectbox("Email de l'utilisateur", options=[user["email"] for user in users])

    if user_email:
        borrowed_books = get_all_borrowed_books(user_email)
        book_titles = [book["book_title"] for book in borrowed_books]
        book_title = st.selectbox("Sélectionnez le livre à retourner", options=book_titles)

        if st.button("Retourner"):
            user = get_user_by_email(user_email)
            book = get_book_by_title(book_title)

            if user and book:
                borrowed_book = next((b for b in user["borrowed_books"] if b["book_title"] == book_title), None)

                if borrowed_book:
                    due_date = borrowed_book["due_date"]
                    if due_date.tzinfo is None:
                        due_date = due_date.replace(tzinfo=timezone.utc)

                    current_time = datetime.now(timezone.utc)

                    if current_time > due_date:
                        st.warning("Retour en retard. Une amende sera appliquée.")
                        fine = (current_time - due_date).days * 2
                        db.collection("users").document(user["id"]).update({"fines": firestore.Increment(fine)})

                    user["borrowed_books"].remove(borrowed_book)
                    db.collection("users").document(user["id"]).update({"borrowed_books": user["borrowed_books"]})

                    book["available_copies"] += 1
                    db.collection("books").document(book["id"]).update({"available_copies": book["available_copies"]})

                    st.success(f"Le livre '{book_title}' a été retourné.")
                else:
                    st.error("Le livre n'a pas été trouvé dans les emprunts de l'utilisateur.")
                    
run()