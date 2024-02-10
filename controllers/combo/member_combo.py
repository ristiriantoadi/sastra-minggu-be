import re

from config.mongo_collection import MEMBER


async def find_all_members(name: str = ""):
    return await MEMBER.find(
        {"name": {"$regex": re.compile(name, re.IGNORECASE)}}
    ).to_list(None)
