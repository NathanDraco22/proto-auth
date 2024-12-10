from fastapi.exceptions import HTTPException
from models import AccountModel, AccountInfo
from tools import (
    is_valid_email,
    generate_uuid5,
    now_in_milliseconds,
    ErrorTexts,
    hash_password,
    verify_password,
    TokenGenerator,
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
        account = AccountModel(
            id=generated_id,
            authProvider="email",
            email=email,
            password=hashed_password,
            createdAt=created_at,
        )
        await self.email_datasource.sign_up_data(account.model_dump())

        access_token, refresh_token = generates_token(account)

        account_info = AccountInfo.model_validate(account.model_dump())
        return SimpleEmailResponse(
            refreshToken=refresh_token,
            accessToken=access_token,
            account=account_info,
        )

    async def sign_in(self, body: CredentialsBody) -> SimpleEmailResponse:
        email, password = body.email, body.password

        if not is_valid_email(email):
            raise HTTPException(status_code=400, detail=ErrorTexts.INVALID_EMAIL)
        account_data = await self.email_datasource.sign_in_data(email)

        if not account_data:
            raise HTTPException(status_code=404, detail=ErrorTexts.EMAIL_NOT_EXISTS)

        account = AccountModel.model_validate(account_data)
        if not verify_password(password, account.password):
            raise HTTPException(status_code=401, detail=ErrorTexts.INVALID_CREDENTIALS)

        access_token, refresh_token = generates_token(account)

        account_info = AccountInfo.model_validate(account.model_dump())
        return SimpleEmailResponse(
            refreshToken=refresh_token,
            accessToken=access_token,
            account=account_info,
        )


def generates_token(account: AccountModel) -> tuple[str, str]:
    """Generate access and refresh tokens, respectively."""
    refresh_token = TokenGenerator.generate_refresh_token(
        account.id,
        {"emailVerified": account.isEmailVerified},
    )
    access_token = TokenGenerator.generate_access_token(
        account.id,
        {"emailVerified": account.isEmailVerified},
    )
    return access_token, refresh_token
