import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Function to initialize Firestore with user-provided credentials
def init_firestore(cred_file):
    try:
        cred = credentials.Certificate(cred_file)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        st.success("Connected to Firestore successfully!")
        return db
    except Exception as e:
        st.error(f"Failed to connect to Firestore: {e}")
        return None

# Function to fetch and display Firestore data
def get_firestore_data(db, collection):
    try:
        docs = db.collection(collection).stream()
        data = [doc.to_dict() for doc in docs]
        if data:
            st.write(f"Data from '{collection}' collection:")
            st.write(data)
        else:
            st.warning(f"No data found in collection '{collection}'.")
    except Exception as e:
        st.error(f"Error fetching data from Firestore: {e}")

# Streamlit app layout
def main():
    st.title("Firestore Connection Page")
    
    # Input for Firebase credentials JSON file
    cred_file = st.file_uploader("Upload Firebase Credentials (JSON)", type=["json"])

    # Input for Firestore collection name
    collection = st.text_input("Enter Firestore Collection Name")
    
    if cred_file and collection:
        # Initialize Firestore and display data
        db = init_firestore(cred_file)
        if db:
            get_firestore_data(db, collection)

if __name__ == "__main__":
    main()
