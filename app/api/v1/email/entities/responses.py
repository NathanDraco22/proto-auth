from pydantic import BaseModel

from models.account_model import AccountInfo


class SimpleEmailResponse(BaseModel):
    accessToken: str
    refreshToken: str
    account: AccountInfo
