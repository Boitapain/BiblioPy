import firebase_admin
from firebase_admin import credentials, firestore
import toml

# Load secrets from the secrets.toml file
secrets = toml.load('./.streamlit/secrets.toml')

# Initialize Firebase
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": secrets['firebase']['type'],
            "project_id": secrets['firebase']['project_id'],
            "private_key_id": secrets['firebase']['private_key_id'],
            "private_key": secrets['firebase']['private_key'].replace("\\n", "\n"),
            "client_email": secrets['firebase']['client_email'],
            "client_id": secrets['firebase']['client_id'],
            "auth_uri": secrets['firebase']['auth_uri'],
            "token_uri": secrets['firebase']['token_uri'],
            "auth_provider_x509_cert_url": secrets['firebase']['auth_provider_x509_cert_url'],
            "client_x509_cert_url": secrets['firebase']['client_x509_cert_url'],
            "universe_domain": secrets['firebase']['universe_domain']
        })
        firebase_admin.initialize_app(cred)

# Firestore client
def get_firestore_client():
    initialize_firebase()
    return firestore.client()