from fastapi import APIRouter

from entities.bodies import GoogleSignInBody

from .google_controller import GoogleController

google_router = APIRouter()

controller = GoogleController()


@google_router.get("/signin")
async def google_signin(body: GoogleSignInBody):
    return controller.sign_in(body)
