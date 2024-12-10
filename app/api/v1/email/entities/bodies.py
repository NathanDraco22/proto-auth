from pydantic import BaseModel

class CredentialsBody(BaseModel):
    email: str
    password: str
