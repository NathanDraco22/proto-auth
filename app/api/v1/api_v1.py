from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from .email.email_router import email_router

app_v1 = FastAPI(
    title="Auth Service API v1",
    description="Auth Service",
    version="1.0.0",
    default_response_class= ORJSONResponse
)


app_v1.include_router(email_router, prefix="/email", tags=["Email"])

