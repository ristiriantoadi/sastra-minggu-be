from config.mongo_collection import MEMBER
from controllers.util.crud import find_one_on_db, insert_one_on_db
from models.user.member import Member


async def find_member_on_db(criteria: dict):
    return await find_one_on_db(collection=MEMBER, criteria=criteria)


async def insert_member_to_db(member: Member):
    return await insert_one_on_db(collection=MEMBER, data=member.dict())
