from datetime import date, datetime

from fastapi import HTTPException

from config.mongo_collection import WORK
from controllers.util.crud import get_list_on_db
from models.default.base import OutputList, PaginationDir
from models.work.work import Work
from models.work.work_enum import WorkTypeEnum


def validate_publication_proof(link: str = None, file: str = None):
    if link == None and file == None:
        raise HTTPException(status_code=400, detail="Bukti publikasi harus diisi")


async def insert_work_to_db(
    title: str,
    author: str,
    workType: WorkTypeEnum,
    media: str,
    publicationDate: date,
    publicationProof: str,
):
    publicationDate = datetime.combine(publicationDate, datetime.min.time())
    data = Work(
        title=title,
        author=author,
        workType=workType,
        media=media,
        publicationDate=publicationDate,
        publicationProof=publicationProof,
    )
    await WORK.insert_one(data.dict())


async def find_works(
    size: int, page: int, sort: str, dir: PaginationDir, criteria: dict
) -> OutputList:
    return await get_list_on_db(collection=WORK, sort=sort, dir=dir, criteria=criteria)
