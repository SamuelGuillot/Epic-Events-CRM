import os
import jwt
import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

SECRET_KEY = "Da_KEY_qui_doit_faire_au_moins_32_caracteres_pour_la_securite"
TOKEN_FILE = ".epic_token"

def save_token(token):
    """Sauvegarde le JWT dans un fichier local."""
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def get_token():
    """Récupère le JWT depuis le fichier local."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None


def clear_token():
    """Supprime le fichier du JWT (déconnexion)."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        return True
    return False

def create_jwt(user_id, email):
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

def hash_password(password):
    """Transforme un mot de passe en clair en un hash sécurisé."""
    
    ph = PasswordHasher()

    return ph.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Vérifie qu'un mot de passe en clair correspond à un hash.
    Retourne True si ça correspond, False sinon.
    """
    try:
        ph = PasswordHasher()
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False