from pydantic import BaseModel
from typing import Literal


AuthProvider = Literal[
    "email",
    "phone",
    "google",
]


class AccountModel(BaseModel):
    id: str
    authProvider: AuthProvider
    email: str | None = None
    phone: str | None = None
    password: str | None = None
    isActive: bool = True
    isEmailVerified: bool = False
    isPhoneVerified: bool = False
    createdAt: int


class AccountInfo(BaseModel):
    id: str
    authProvider: AuthProvider
    email: str | None = None
    phone: str | None = None
    isActive: bool = True
    isEmailVerified: bool = False
    isPhoneVerified: bool = False
    createdAt: int
