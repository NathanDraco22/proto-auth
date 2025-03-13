from .entities.bodies import GoogleSignInBody
from .tools.google_token import verify_google_token


class GoogleController:

    async def sign_in(self, body: GoogleSignInBody):
        res = verify_google_token(body.token)
        print(res)
        return True
