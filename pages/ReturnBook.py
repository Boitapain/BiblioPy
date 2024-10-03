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
        borrowed_books = get_borrowed_books(user_email)
        borrowed_books_list = list(borrowed_books)

        if not borrowed_books_list:
            st.warning("Aucun livre emprunté trouvé pour cet utilisateur.")
            return
            
        book_titles = [book["book_title"] for book in borrowed_books_list]
        book_title = st.selectbox("Sélectionnez le livre à retourner", options=book_titles)

        if st.button("Retourner"):
            user = get_user_by_email(user_email)
            if user:
                borrowed_book = next((b for b in borrowed_book_list if b.get("book_title") == book_title), None)

            if borrowed_book:
                borrowed_entry_id = borrowed_book.id

            due_date = borrowed_book.get("due_date")

            if due_date.tzinfo is None:
                due_date = due_date.replace(tzinfo=timezone.utc)

            current_time = datetime.now(timezone.utc)
            
                    if current_time > due_date:
                        st.warning("Retour en retard. Une amende sera appliquée.")
                        fine = (current_time - due_date).days * 2
                        db.collection("users").document(user["id"]).update({"fines": firestore.Increment(fine)})

                    db.collection("emprunt").document(borrowed_entry_id).update({
                        "status": "returned",
                        "fine": fine
                    })

               book = get_book_by_title(book_title)
            if book:
                    book["available_copies"] += 1
                    db.collection("books").document(book["id"]).update({"available_copies": book["available_copies"]})

                    st.success(f"Le livre '{book_title}' a été retourné.")
                else:
                    st.error("Le livre n'a pas été trouvé dans les emprunts de l'utilisateur.")
        else:
            st.error("Utilisateur non trouvé.")
                    
run()
