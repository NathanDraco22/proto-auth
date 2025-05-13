from pydantic import BaseModel
from typing import Literal

AuthProvider = Literal[
    "email",
    "phone",
    "google",
]


class AccountInfo(BaseModel):
    id: str
    authProvider: AuthProvider
    name: str | None = None
    picture: str | None = None
    email: str | None = None
    phone: str | None = None
    isActive: bool = True
    isEmailVerified: bool = False
    isPhoneVerified: bool = False
    lastLogin: int | None = None
    createdAt: int
    updatedAt: int | None = None
