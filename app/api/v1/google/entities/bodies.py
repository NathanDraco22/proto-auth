from pydantic import BaseModel


class GoogleSignInBody(BaseModel):
    token: str
