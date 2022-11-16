from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def get_password_hash(password: str) -> str:
    return pass_context(password)