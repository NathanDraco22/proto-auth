import os
from datetime import datetime, timedelta
from typing import Any, Literal, TypedDict
import jwt

from .time_tools import now_in_seconds, in_one_month

TokenType = Literal["REFRESH", "ACCESS", "ID"]


class Claims(TypedDict):
    type: TokenType
    sub: str
    iat: int
    exp: int


class TokenGenerator:

    @staticmethod
    def generate_refresh_token(
        user_id: str,
        payload: dict[str, Any] | None = None,
    ) -> str:
        claims: Claims = {
            "type": "REFRESH",
            "sub": user_id,
            "iat": now_in_seconds(),
            "exp": in_one_month(),
        }
        if payload is not None:
            claims = {**claims, **payload}
        secret = os.getenv("REFRESH_TOKEN_SECRET")
        token = jwt.encode(claims, secret, algorithm="HS256")
        return token

    @staticmethod
    def generate_access_token(
        user_id: str,
        payload: dict[str, Any] | None = None,
    ) -> str:
        access_token_exp = access_token_exp_in_seconds()
        claims: Claims = {
            "type": "REFRESH",
            "sub": user_id,
            "iat": now_in_seconds(),
            "exp": access_token_exp,
        }
        if payload is not None:
            claims = {**claims, **payload}
        secret = os.getenv("ACCESS_TOKEN_SECRET")
        token = jwt.encode(claims, secret, algorithm="HS256")
        return token

    def generate_id_token(self):
        pass


def access_token_exp_in_seconds() -> int:
    now = datetime.now()
    in_seconds = int((now + timedelta(days=1)).timestamp())
    return in_seconds
