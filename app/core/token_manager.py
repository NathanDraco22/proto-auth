import os
from datetime import datetime, timedelta
from typing import Any, Literal, TypedDict

import jwt
from cryptography.hazmat.primitives import serialization

from tools.time_tools import now_in_seconds, in_one_month

TokenType = Literal["REFRESH", "ACCESS", "ID"]

TOKEN_ALGORITHM = "EdDSA"


class Claims(TypedDict):
    type: TokenType
    sub: str
    iat: int
    exp: int


class TokenManager:
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

        full_claims = {}

        if payload is not None:
            full_claims = {**claims, **payload}

        refresh_token_key = get_refresh_token_private_key()

        token = jwt.encode(
            full_claims,
            refresh_token_key,  # type: ignore
            algorithm=TOKEN_ALGORITHM,
        )

        return token

    @staticmethod
    def generate_access_token(
        user_id: str,
        payload: dict[str, Any] | None = None,
    ) -> str:
        access_token_exp = access_token_exp_in_seconds()

        claims: Claims = {
            "type": "ACCESS",
            "sub": user_id,
            "iat": now_in_seconds(),
            "exp": access_token_exp,
        }

        full_claims = {}
        if payload is not None:
            full_claims = {**claims, **payload}

        access_token_key = get_access_token_private_key()

        token = jwt.encode(
            full_claims,
            access_token_key,  # type: ignore
            algorithm=TOKEN_ALGORITHM,
        )

        return token

    @staticmethod
    def verify_token(token: str) -> Any:
        payload = jwt.decode(token, options={"verify_signature": False})

        key = (
            get_refresh_token_public_key()
            if payload["type"] == "REFRESH"
            else get_access_token_public_key()
        )

        result = jwt.decode(
            token,
            key,  # type: ignore
            algorithms=[TOKEN_ALGORITHM],
            options={"require": ["exp", "sub"]},
        )

        return result


def access_token_exp_in_seconds() -> int:
    now = datetime.now()
    in_seconds = int((now + timedelta(days=1)).timestamp())

    return in_seconds


def get_refresh_token_private_key():
    private = os.environ["REFRESH_TOKEN_PRIVATE_KEY"]
    priv_key = serialization.load_pem_private_key(
        private.encode("utf-8"), password=None
    )

    return priv_key


def get_access_token_private_key():
    private = os.environ["ACCESS_TOKEN_PRIVATE_KEY"]
    priv_key = serialization.load_pem_private_key(
        private.encode("utf-8"), password=None
    )

    return priv_key


def get_refresh_token_public_key():
    public = os.environ["REFRESH_TOKEN_PUBLIC_KEY"]
    public_key = serialization.load_pem_public_key(public.encode("utf-8"))
    return public_key


def get_access_token_public_key():
    public = os.environ["ACCESS_TOKEN_PUBLIC_KEY"]
    public_key = serialization.load_pem_public_key(public.encode("utf-8"))

    return public_key
