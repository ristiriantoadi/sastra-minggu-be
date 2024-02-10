from datetime import date, datetime

from fastapi import HTTPException, UploadFile

from config.mongo_collection import WORK
from controllers.util.crud import get_list_on_db
from controllers.util.upload_file import upload_file
from models.authentication.authentication import TokenData
from models.default.base import OutputListPagination, PaginationDir
from models.work.work import Work
from models.work.work_enum import WorkTypeEnum


def validate_publication_proof_must_exist(link: str = None, file: str = None):
    if link == None and file == None:
        raise HTTPException(status_code=400, detail="Bukti publikasi harus diisi")


async def upload_publication_proof(publicationProofFile: UploadFile):
    return await upload_file(file=publicationProofFile, featureFolder="work")


async def insert_work_to_db(
    title: str,
    author: str,
    workType: WorkTypeEnum,
    media: str,
    publicationDate: date,
    currentUser: TokenData,
    publicationProofLink: str = None,
    publicationProofFile: UploadFile = None,
):
    publicationDate = datetime.combine(publicationDate, datetime.min.time())
    if publicationProofLink is None:
        publicationProofLink = await upload_publication_proof(publicationProofFile)
    data = Work(
        creatorId=currentUser.userId,
        title=title,
        author=author,
        workType=workType,
        media=media,
        publicationDate=publicationDate,
        publicationProof=publicationProofLink,
    )
    await WORK.insert_one(data.dict())


async def find_works(
    size: int, page: int, sort: str, dir: PaginationDir, criteria: dict
) -> OutputListPagination:
    return await get_list_on_db(
        collection=WORK, sort=sort, dir=dir, criteria=criteria, size=size, page=page
    )


def add_additional_data_works(data: dict, currentUser: TokenData):
    for d in data:
        if str(d["creatorId"]) == currentUser.userId:
            d["isEditable"] = True
    return data
