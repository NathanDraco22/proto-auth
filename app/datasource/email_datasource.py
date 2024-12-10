from typing import Any
from service import MongoService, mongo_service


class EmailDataSource:

    def __init__(self, db_service: MongoService):
        self.db_service = db_service
        pass

    async def sign_up_data(self, data: dict[str, Any]) -> dict[str, Any]:
        col = self.db_service.get_email_collection()
        await col.insert_one(data)
        return data

    async def sign_in_data(self, email: str) -> dict[str, Any] | None:
        col = self.db_service.get_email_collection()
        res = await col.find_one({"email": email})
        return res

    async def if_email_exists(self, email: str) -> bool:
        col = self.db_service.get_email_collection()
        res = await col.find_one({"email": email})
        return res is not None


email_datasource = EmailDataSource(mongo_service)
