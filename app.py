import streamlit as st
import toml
from firebase_admin import credentials, initialize_app

# Load secrets from the secrets.toml file
secrets = toml.load('./.streamlit/secrets.toml')

# Initialize Firebase
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

initialize_app(cred)

st.title("BiblioPy Streamlit App")
st.write("Connected to Firebase successfully!")
