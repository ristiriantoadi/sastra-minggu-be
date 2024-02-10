from beanie import PydanticObjectId

from config.mongo_collection import COUNT_NOTIF
from models.authentication.authentication import TokenData


async def increment_count_notifs(authorId: str):
    countNotif = await COUNT_NOTIF.find_one({"userId": PydanticObjectId(authorId)})
    if countNotif:
        updateData = {"count": countNotif["count"] + 1}
        await COUNT_NOTIF.update_one(
            {"userId": PydanticObjectId(authorId)},
            {"$set": updateData},
        )
    else:
        await COUNT_NOTIF.insert_one({"userId": PydanticObjectId(authorId), "count": 1})


async def get_notif_counts(currentUser: TokenData):
    notif = await COUNT_NOTIF.find_one({"userId": PydanticObjectId(currentUser.userId)})
    if notif is None:
        return 0
    return notif["count"]


async def reset_notif_counts(currentUser: TokenData):
    await COUNT_NOTIF.update_one(
        {"userId": PydanticObjectId(currentUser.userId)},
        {"$set": {"count": 0}},
    )
