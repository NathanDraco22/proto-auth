from fastapi import HTTPException, status
from models import GoogleAccountModel
from core import generate_uuid5
from datasource import GoogleAccountDatasource
from tools import now_in_milliseconds, generate_token

from .entities import (
    GoogleSignInBody,
    GoogleTokenClaims,
    GoogleAuthResponse,
)
from .utils.google_token import verify_google_token


class GoogleController:

    def __init__(self, google_account_ds: GoogleAccountDatasource):
        self.google_account_ds = google_account_ds

    async def sign_in(self, body: GoogleSignInBody) -> GoogleAuthResponse:
        res = verify_google_token(body.token)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token",
            )

        payload_token = GoogleTokenClaims.model_validate(res)

        google_account_id = payload_token.sub
        account_data = await self.google_account_ds.sign_in_data(google_account_id)
        if account_data is None:
            return await self.__create_account(payload_token)

        account_model = GoogleAccountModel.model_validate(account_data)
        return await self.__sign_in(account_model)

    async def __create_account(
        self, payload_token: GoogleTokenClaims
    ) -> GoogleAuthResponse:
        created_at = now_in_milliseconds()
        generated_id = generate_uuid5(payload_token.email, created_at)
        account_model = GoogleAccountModel(
            id=generated_id,
            name=payload_token.name,
            picture=payload_token.picture,
            email=payload_token.email,
            googleAccountId=payload_token.sub,
            isEmailVerified=payload_token.email_verified,
            createdAt=created_at,
        )

        account_data = account_model.model_dump()
        await self.google_account_ds.sign_up_account_data(account_data)

        access_token, refresh_token = generate_token(account_model)

        await self.google_account_ds.update_last_login(
            account_model.id,
            account_model.createdAt,
        )

        response = GoogleAuthResponse(
            refreshToken=refresh_token,
            accessToken=access_token,
            account=account_model,
        )
        return response

    async def __sign_in(self, account_model: GoogleAccountModel) -> GoogleAuthResponse:

        access_token, refresh_token = generate_token(account_model)

        await self.google_account_ds.update_last_login(
            account_model.id,
            account_model.createdAt,
        )

        response = GoogleAuthResponse(
            refreshToken=refresh_token,
            accessToken=access_token,
            account=account_model,
        )
        return response
