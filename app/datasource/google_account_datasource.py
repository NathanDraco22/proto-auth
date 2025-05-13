from typing import Any
from service import MongoService, mongo_service


class GoogleAccountDatasource:
    def __init__(self, db_service: MongoService):
        self.db_service = db_service

    async def sign_up_account_data(self, data: dict[str, Any]) -> dict[str, Any]:
        col = self.db_service.get_google_account_collection()
        await col.insert_one(data)
        return data

    async def sign_in_data(self, google_account_id: str) -> dict[str, Any] | None:
        col = self.db_service.get_google_account_collection()
        res = await col.find_one({"googleAccountId": google_account_id})
        return res

    async def update_last_login(self, id: str, last_login: int) -> None:
        col = self.db_service.get_email_collection()
        await col.update_one({"id": id}, {"$set": {"lastLogin": last_login}})

    async def get_account_by_google_account_id(
        self, google_account_id: str
    ) -> dict[str, Any] | None:
        col = self.db_service.get_google_account_collection()
        res = await col.find_one({"googleAccountId": google_account_id})
        return res


google_account_datasource = GoogleAccountDatasource(mongo_service)
