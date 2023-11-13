from datetime import datetime
from typing import List

from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from models.authentication.authentication import TokenData


async def find_one_on_db(collection: AsyncIOMotorCollection, criteria: dict):
    criteria["isDelete"] = False
    return await collection.find_one(criteria)


async def insert_one_on_db(
    collection: AsyncIOMotorCollection, data: dict, currentUser: TokenData = None
):
    data["createTime"] = datetime.utcnow()
    if currentUser:
        data["creatorId"] = currentUser.userId
    op = await collection.insert_one(data)
    return await collection.find_one(op.inserted_id)


async def insert_many_on_db(collection: AsyncIOMotorCollection, data: List[dict]):
    if len(data) == 0:
        return
    op = await collection.insert_many(data)


async def get_list_on_db(
    collection: AsyncIOMotorCollection,
    sort: str = "createTime",
    dir: int = -1,
    criteria: dict = {},
):
    criteria["isDelete"] = False
    cursor = collection.find(criteria).sort(sort, dir)
    data = await cursor.to_list(length=None)
    return {
        "data": data,
    }


async def get_count_on_db(
    collection: AsyncIOMotorCollection,
    criteria: dict = {},
):
    criteria["isDelete"] = False
    return await collection.count_documents(criteria)


async def update_on_db(
    collection: AsyncIOMotorCollection,
    updateData: dict,
    currentUser: TokenData,
    criteria: dict = {},
):
    updateData["updateTime"] = datetime.utcnow()
    updateData["updaterId"] = PydanticObjectId(currentUser.userId)

    criteria["isDelete"] = False
    await collection.update_one(criteria, {"$set": updateData})


async def delete_on_db(
    collection: AsyncIOMotorCollection, criteria: dict, currentUser: TokenData
):
    await collection.update_one(
        criteria,
        {
            "$set": {
                "deleteTime": datetime.utcnow(),
                "deleterId": currentUser.userId,
                "isDelete": True,
            }
        },
    )
