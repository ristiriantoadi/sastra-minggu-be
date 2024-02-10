from beanie import PydanticObjectId

from config.mongo_collection import COUNT_NOTIF
from models.authentication.authentication import TokenData


async def increment_count_notifs(currentUser: TokenData):
    await COUNT_NOTIF.update_one(
        {"userId": PydanticObjectId(currentUser.userId)},
        {"$inc": {"count": 1}},
        upsert=True,
    )
