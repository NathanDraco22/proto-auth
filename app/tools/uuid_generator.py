import os
import uuid


def generate_uuid4():
    return str(uuid.uuid4())


def generate_uuid5(email: str, timestamp: int) -> str:
    keyword = os.getenv("UUID_KEYWORD")
    name = f"{keyword}/{email}-{timestamp}"
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
