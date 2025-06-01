from fastapi.exceptions import HTTPException
from models import EmailAccountModel
from tools import is_valid_email, now_in_milliseconds, ErrorTexts, generate_token

from core import (
    generate_uuid5,
    hash_password,
    verify_password,
)

from datasource import EmailDataSource
from .entities.bodies import CredentialsBody
from .entities.responses import SimpleEmailResponse


class EmailController:

    def __init__(self, email_datasource: EmailDataSource) -> None:
        self.email_datasource = email_datasource

    async def create_account(self, body: CredentialsBody) -> SimpleEmailResponse:
        email, password = body.email, body.password

        if not is_valid_email(email):
            raise HTTPException(status_code=400, detail=ErrorTexts.INVALID_EMAIL)

        is_exists = await self.email_datasource.if_email_exists(email)
        if is_exists:
            raise HTTPException(status_code=409, detail=ErrorTexts.EMAIL_EXISTS)

        created_at = now_in_milliseconds()
        generated_id = generate_uuid5(email, created_at)
        hashed_password = hash_password(password)
        account = EmailAccountModel(
            id=generated_id,
            authProvider="email",
            email=email,
            password=hashed_password,
            createdAt=created_at,
        )
        await self.email_datasource.sign_up_data(account.model_dump())

        access_token, refresh_token = generate_token(account)

        await self.email_datasource.update_last_login(account.id, account.createdAt)

        return SimpleEmailResponse(
            refreshToken=refresh_token,
            accessToken=access_token,
            account=account,
        )

    async def sign_in(self, body: CredentialsBody) -> SimpleEmailResponse:
        email, password = body.email, body.password

        if not is_valid_email(email):
            raise HTTPException(status_code=400, detail=ErrorTexts.INVALID_EMAIL)
        account_data = await self.email_datasource.sign_in_data(email)

        if not account_data:
            raise HTTPException(status_code=404, detail=ErrorTexts.EMAIL_NOT_EXISTS)

        account = EmailAccountModel.model_validate(account_data)
        if not verify_password(password, account.password):
            raise HTTPException(status_code=401, detail=ErrorTexts.INVALID_CREDENTIALS)

        access_token, refresh_token = generate_token(account)

        await self.email_datasource.update_last_login(account.id, account.createdAt)

        return SimpleEmailResponse(
            refreshToken=refresh_token,
            accessToken=access_token,
            account=account,
        )
