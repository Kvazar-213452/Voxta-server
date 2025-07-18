import secrets
import string

token: str

def generate_secure_token(length: int = 15) -> str:
    global token
    chars = string.ascii_letters + string.digits
    return''.join(secrets.choice(chars) for _ in range(length))

def get_token() -> str:
    return token
