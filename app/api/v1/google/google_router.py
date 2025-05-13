from fastapi import APIRouter
from datasource import google_account_datasource

from .entities.bodies import GoogleSignInBody

from .google_controller import GoogleController

google_router = APIRouter()

controller = GoogleController(google_account_datasource)


@google_router.post("/signin")
async def google_signin(body: GoogleSignInBody):
    return await controller.sign_in(body)
