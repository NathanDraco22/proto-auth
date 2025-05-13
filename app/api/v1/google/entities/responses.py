from pydantic import BaseModel

from models.email_account_model import AccountInfo


class GoogleAuthResponse(BaseModel):
    accessToken: str
    refreshToken: str
    account: AccountInfo
