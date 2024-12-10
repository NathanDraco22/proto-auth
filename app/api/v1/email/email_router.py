from fastapi import APIRouter
from .entities.bodies import CredentialsBody
from .entities.responses import SimpleEmailResponse
from .email_controller import EmailController
from datasource import email_datasource
from .metadata import (
    create_simple_meta,
    signin_meta,
    create_2fa_meta,
    verify_code_meta,
    request_code_meta,
)

email_router = APIRouter()

controller = EmailController(email_datasource)


@email_router.post("/signup", **create_simple_meta)
async def create_account(body: CredentialsBody) -> SimpleEmailResponse:
    return await controller.create_account(body)


@email_router.post("/signin", **signin_meta)
async def sign_in(body: CredentialsBody) -> SimpleEmailResponse:
    return await controller.sign_in(body)


@email_router.post("/2fa", **create_2fa_meta)
async def create_account_with_2fa(body: CredentialsBody):
    return {"message": "Email sent"}


@email_router.post("/request-code", **request_code_meta)
async def request_code(body: CredentialsBody):
    return {"message": "Email sent"}


@email_router.post("/verify", **verify_code_meta)
async def verify_2fa():
    return {"message": "Email sent"}
