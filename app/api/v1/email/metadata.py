from tools import EndpointMetadata, ErrorTexts


create_simple_meta: EndpointMetadata = {
    "description": "Create an Account using only email and password",
    "responses": {
        200: {"description": "Account Created"},
        400: {
            "description": "Invalid Email Format",
            "content": {
                "application/json": {
                    "example": ErrorTexts.INVALID_EMAIL,
                },
            },
        },
        401: {
            "description": "Invalid Credentials",
            "content": {
                "application/json": {
                    "example": ErrorTexts.INVALID_CREDENTIALS,
                },
            },
        },
        409: {
            "description": "Email Already Exists",
            "content": {
                "application/json": {
                    "example": ErrorTexts.EMAIL_EXISTS,
                },
            },
        },
    },
}

signin_meta: EndpointMetadata = {
    "description": "Create an Account using only email and password",
    "responses": {
        200: {"description": "Sign In Success"},
        400: {
            "description": "Invalid Email Format",
            "content": {
                "application/json": {
                    "example": ErrorTexts.INVALID_EMAIL,
                },
            },
        },
        401: {
            "description": "Invalid Credentials",
            "content": {
                "application/json": {
                    "example": ErrorTexts.INVALID_CREDENTIALS,
                },
            },
        },
        404: {
            "description": "Email Not Found",
            "content": {
                "application/json": {
                    "example": ErrorTexts.EMAIL_NOT_EXISTS,
                },
            },
        },
    },
}

create_2fa_meta: EndpointMetadata = {
    "description": "Create an Account "
    + "with email, password and 2FA, \n"
    + "Send a OTP with expiration time (90 seconds) to the user's email"
}

request_code_meta: EndpointMetadata = {
    "description": "Send a OTP with expiration time (90 seconds) to the user's email"
}

verify_code_meta: EndpointMetadata = {
    "description": "Verify the OTP sent to the user's email"
}
