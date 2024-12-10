from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from dotenv import load_dotenv

from app_lifespan import lifespan
from api.v1.api_v1 import app_v1

load_dotenv()

app = FastAPI(
    title="Auth Service",
    description="Auth Service",
    version="0.0.1",
    default_response_class= ORJSONResponse,
    lifespan=lifespan,
)

app.mount("/api/v1", app_v1)
