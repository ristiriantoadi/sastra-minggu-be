import asyncio

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from config.config import DB


class MongoConnect:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            logger.info(f"Initialize mongo instance connection")
            # client = AsyncIOMotorClient(
            #     "mongodb+srv://ristiriantoadi:NBAg6WESr4M%3E6nY@cluster0.rurgtmw.mongodb.net/"
            # )
            client = AsyncIOMotorClient("mongodb://localhost:27017/")
            client.get_io_loop = asyncio.get_event_loop
            cls.__instance = client
            return client
        else:
            logger.info(f"Use exsisting mongo instance connection: {cls.__instance}")
            return cls.__instance

    def __init__(self):
        self.__instance = None

    def close(self):
        logger.info(f"Close mongo instance connection: {self.__instance}")
        self.__instance.close()


MGDB_CLIENT = MongoConnect()
MGDB_SASTRA_MINGGU = MGDB_CLIENT[DB]
