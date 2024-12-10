from contextlib import asynccontextmanager
from service import mongo_service


async def init_services():
    await mongo_service.init_service()


@asynccontextmanager
async def lifespan(app):
    await init_services()
    yield
