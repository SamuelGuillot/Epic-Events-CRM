import os
import jwt
import datetime

SECRET_KEY = "Da_KEY_qui_doit_faire_au_moins_32_caracteres_pour_la_securite"
TOKEN_FILE = ".epic_token"


def create_jwt(user_id, email):
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None


def clear_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        return True
    return False