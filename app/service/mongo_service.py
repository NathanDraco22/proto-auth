from typing import Any
from pymongo import IndexModel
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from tools import get_mongo_url, get_db_name

EMAIL_COLLECTION = "email"


class MongoService:

    _mongo: AsyncIOMotorClient[dict[str, Any]]
    _db: AsyncIOMotorDatabase

    async def init_service(self):
        mongo_url = get_mongo_url()
        db_name = get_db_name()
        self._mongo = AsyncIOMotorClient(mongo_url)
        self._db = self._mongo.get_database(db_name)
        await self.create_indexes()

    async def create_indexes(self):
        email_collection = self._db.get_collection(EMAIL_COLLECTION)
        await email_collection.create_indexes(
            [
                IndexModel([("email", 1)], unique=False),
                IndexModel([("phone", 1)], unique=False),
                IndexModel([("id", 1)], unique=True),
                IndexModel([("authProvider", 1)], unique=False),
            ]
        )

    def get_email_collection(self) -> AsyncIOMotorCollection[dict[str, Any]]:
        return self._db.get_collection(EMAIL_COLLECTION)


mongo_service = MongoService()
