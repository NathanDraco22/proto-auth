import os
from typing import Any
from google.oauth2 import id_token
from google.auth.transport import requests


def verify_google_token(token: str) -> dict[str, Any] | None:
    try:
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            google_client_id,
        )
        return idinfo
    except Exception:
        return None
