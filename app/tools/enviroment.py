import os
from tools.app_logger import AppLogger

def get_mongo_url() -> str:
    url = os.getenv("MONGO_URL")
    if url is None:
        AppLogger.critical("MONGO_URL not set")
        raise Exception("MONGO_URL not set")
    return url

def get_db_name() -> str:
    db_name = os.getenv("DB_NAME")
    if db_name is None:
        AppLogger.warning("DB_NAME not set, using default name 'accounts'")
        db_name = "accounts"
    return db_name