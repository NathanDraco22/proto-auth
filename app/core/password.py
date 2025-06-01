import base64
from argon2 import PasswordHasher


def hash_password(password: str) -> str:
    ph = PasswordHasher()
    hassed_password = ph.hash(password)
    base64_password = base64.b64encode(bytes(hassed_password, encoding="utf-8"))
    return str(base64_password, encoding="utf-8")


def verify_password(password: str, hassed_password: str) -> bool:
    hassed_password = str(base64.b64decode(hassed_password), encoding="utf-8")
    ph = PasswordHasher()
    try:
        ph.verify(hassed_password, password)
    except Exception:
        return False
    return True
