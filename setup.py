import getpass
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv()

#Encryption setup
# Generate and save a key
def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

# Load the key
def load_key():
    return open("secret.key", "rb").read()


# Encrypt text
def encrypt_text(text):
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(text.encode())

# Decrypt text
def decrypt_text(encrypted_text):
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_text).decode()

# Authentication
def authenticate():
    correct_password = os.environ.get("PASSWORD")  # Set your password here
    password = getpass.getpass("Enter your password: ")
    if password == correct_password:
        print("Access Granted!")
        return True
    else:
        print("Access Denied!")
        return False