import streamlit as st
import toml
import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

# Load secrets from the secrets.toml file
secrets = toml.load('./.streamlit/secrets.toml')

if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": secrets['firebase']['type'],
        "project_id": secrets['firebase']['project_id'],
        "private_key_id": secrets['firebase']['private_key_id'],
        "private_key": secrets['firebase']['private_key'].strip(),
        "client_email": secrets['firebase']['client_email'],
        "client_id": secrets['firebase']['client_id'],
        "auth_uri": secrets['firebase']['auth_uri'],
        "token_uri": secrets['firebase']['token_uri'],
        "auth_provider_x509_cert_url": secrets['firebase']['auth_provider_x509_cert_url'],
        "client_x509_cert_url": secrets['firebase']['client_x509_cert_url'],
        "universe_domain": secrets['firebase']['universe_domain']
    })

    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("BiblioPy")
st.write("Connected to Firebase successfully!")

# Limite de prêt par utilisateur
MAX_BORROW_LIMIT = 3

# Main Page
def main():
    menu = ["Accueil", "Ajouter un livre", "Ajouter un utilisateur", "Emprunter un livre", "Retourner un livre", "Statistiques"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Accueil":
        st.subheader("Bienvenue à BiblioPy")
        display_books()

    elif choice == "Ajouter un livre":
        add_book()

    elif choice == "Ajouter un utilisateur":
        add_user()

    elif choice == "Emprunter un livre":
        borrow_book()

    elif choice == "Retourner un livre":
        return_book()

    elif choice == "Statistiques":
        show_statistics()

# Ajouter un livre 
def add_book():
    st.subheader("Ajouter un nouveau livre")
    title = st.text_input("Titre du livre")
    author = st.text_input("Auteur du livre")
    isbn = st.text_input("ISBN")
    available_copies = st.number_input("Nombre de copies disponibles", min_value=1, step=1)
    
    if st.button("Ajouter livre"):
        book_data = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "available_copies": available_copies,
            "borrowed_by": []  # Keep track of who has borrowed the book
        }
        db.collection("books").add(book_data)  # Writing to Firestore
        st.success(f"Le livre '{title}' a été ajouté avec succès !")

# Ajouter un utilisateur 
def add_user():
    st.subheader("Ajouter un nouvel utilisateur")
    name = st.text_input("Nom de l'utilisateur")
    email = st.text_input("Email de l'utilisateur")

    if st.button("Ajouter utilisateur"):
        user_data = {
            "name": name,
            "email": email,
            "borrowed_books": [],
            "fines": 0
        }
        db.collection("users").add(user_data)
        st.success(f"L'utilisateur '{name}' a été ajouté avec succès !")

# Emprunter un livre 
def borrow_book():
    st.subheader("Emprunter un livre")
    
    #populate selectbox
    users = get_all_users()
    books = get_all_borrowable_books()
    
    user_email = st.selectbox("Email de l'utilisateur",options=[user["email"] for user in users])
    book_title = st.selectbox("Titre du livre", options=[book["title"] for book in books])

    if st.button("Emprunter"):
        user = get_user_by_email(user_email)
        book = get_book_by_title(book_title)

        if user and book:
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
                # Mise à jour des informations de l'utilisateur et du livre
                due_date = datetime.now() + relativedelta(weeks=2)
                user["borrowed_books"].append({"book_title": book_title, "due_date": due_date})
                db.collection("users").document(user["id"]).update({"borrowed_books": user["borrowed_books"]})

                book["available_copies"] -= 1
                db.collection("books").document(book["id"]).update({"available_copies": book["available_copies"]})
                
                st.success(f"Le livre '{book_title}' a été emprunté avec succès par {user_email}. Retour prévu le {due_date.strftime('%d-%m-%Y')}")
        else:
            st.warning("Le mail ou le livre n'existe pas")

# Retourner un livre
def return_book():
    st.subheader("Retourner un livre")
    
    users = get_all_users()
    
    user_email = st.selectbox("Email de l'utilisateur",options=[user["email"] for user in users])
    
    if user_email :
        borrowed_books = get_all_borrowed_books(user_email)
        
        book_titles = [book["book_title"] for book in borrowed_books]
        book_title = st.selectbox("Sélectionnez le livre à retourner", options=book_titles)
    
        if st.button("Retourner"):
            user = get_user_by_email(user_email)
            book = get_book_by_title(book_title)

            if user and book:
                borrowed_books = user["borrowed_books"]
                borrowed_book = next((b for b in borrowed_books if b["book_title"] == book_title), None)

                if borrowed_book:
                    # Vérification de la date de retour
                    due_date = borrowed_book["due_date"]

                    if due_date.tzinfo is None:
                        due_date = due_date.replace(tzinfo=timezone.utc)  

                    current_time = datetime.now(timezone.utc)

                    if current_time > due_date:
                        st.warning("Retour en retard. Une amende sera appliquée.")
                        fine = (current_time - due_date).days * 2  
                        # Amende de 2 unités par jour de retard


                    borrowed_books.remove(borrowed_book)
                    db.collection("users").document(user["id"]).update({"borrowed_books": borrowed_books, "fines": user["fines"]})

                    # Mise à jour du stock de livres
                    book["available_copies"] += 1
                    db.collection("books").document(book["id"]).update({"available_copies": book["available_copies"]})

                    st.success(f"Le livre '{book_title}' a été retourné.")
                else:
                    st.error("Le livre n'a pas été trouvé dans les emprunts de l'utilisateur.")

# Récupérer un utilisateur par email
def get_user_by_email(email):
    user_ref = db.collection("users").where("email", "==", email).stream()
    user = None
    for u in user_ref:
        user = u.to_dict()
        user["id"] = u.id   
    return user

# Récupérer tous les utilisateurs
def get_all_users():
    users_ref = db.collection("users")
    return [user.to_dict() for user in users_ref.stream()]

# Récupérer un livre par titre 
def get_book_by_title(title):
    books_ref = db.collection("books").where("title", "==", title).stream()
    book = None 
    for b in books_ref:
        book = b.to_dict()
        book["id"] = b.id
    return book

# Récupérer tous les livres
def get_all_borrowable_books():
    books_ref = db.collection("books").where("available_copies", ">" ,0).stream()
    return [book.to_dict() for book in books_ref]

# Récupérer tous les livres empruntés d'un utilisateur
def get_all_borrowed_books(user_email):
    user = get_user_by_email(user_email)
    books_borrowed = user["borrowed_books"]
    
    return books_borrowed

# Afficher la liste des livres
def display_books():
    st.subheader("Liste des livres")
    books_ref = db.collection("books").stream()

    st.write("---")
    # Loop through each book and create a row for its details
    for book in books_ref:
        book_data = book.to_dict()
        cols = st.columns(4)  # Create 4 columns for each book's details

        with cols[0]:
            st.write(f"**Titre:** {book_data['title']}")
        with cols[1]:
            st.write(f"**Auteur:** {book_data['author']}")
        with cols[2]:
            st.write(f"**ISBN:** {book_data['isbn']}")
        with cols[3]:
            st.write(f"**Copies disponibles:** {book_data['available_copies']}")

        st.write("---")  # Separator for clarity
# Statistiques
def show_statistics():
    st.subheader("Statistiques")
    # Affichage des statistiques 
    borrowed_books_ref = db.collection("books").stream()
    for book in borrowed_books_ref:
        book_data = book.to_dict()
        st.write(f"{book_data['title']}: {len(book_data['borrowed_by'])} emprunts")

if __name__ == '__main__':
    main()
