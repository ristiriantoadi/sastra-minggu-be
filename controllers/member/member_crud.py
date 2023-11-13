
from config.mongo_collection import MEMBER
from controllers.util.crud import find_one_on_db


async def find_member_on_db(criteria: dict):
    return await find_one_on_db(collection=MEMBER, criteria=criteria)
