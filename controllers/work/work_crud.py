from datetime import date, datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, UploadFile

from config.mongo_collection import WORK
from controllers.member.member_crud import find_member_on_db
from controllers.util.crud import delete_on_db, get_list_on_db, update_on_db
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
    authorId: str = None,
):
    publicationDate = datetime.combine(publicationDate, datetime.min.time())
    if publicationProofLink is None:
        publicationProofLink = await upload_publication_proof(publicationProofFile)
    data = Work(
        createTime=datetime.utcnow(),
        creatorId=currentUser.userId,
        title=title,
        author=author,
        workType=workType,
        media=media,
        publicationDate=publicationDate,
        publicationProof=publicationProofLink,
        authorId=authorId,
    )
    await WORK.insert_one(data.dict())


async def find_works(
    size: int, page: int, sort: str, dir: PaginationDir, criteria: dict
) -> OutputListPagination:
    return await get_list_on_db(
        collection=WORK, sort=sort, dir=dir, criteria=criteria, size=size, page=page
    )


async def add_additional_data_works(data: dict, currentUser: TokenData):
    for d in data:
        if str(d["creatorId"]) == currentUser.userId:
            d["isEditable"] = True
        if "authorId" in d:
            if d["authorId"]:
                member = await find_member_on_db(
                    {"_id": PydanticObjectId(d["authorId"])}
                )
                d["author"] = f"{d['author']} (@{member['username']})"
    return data


def get_filter_list_work(
    title: str = None,
    author: str = None,
    workType: WorkTypeEnum = None,
    media: str = None,
    startDate: date = None,
    endDate: date = None,
):
    filter = {}
    if title:
        filter["title"] = title
    if author:
        filter["author"] = author
    if workType:
        filter["workType"] = workType
    if media:
        filter["media"] = media
    if startDate and endDate:
        startDate = datetime.combine(startDate, datetime.min.time())
        endDate = datetime.combine(endDate, datetime.max.time())
        filter["publicationDate"] = {"$gte": startDate, "$lte": endDate}
    return filter


async def delete_work(workId: str, currentUser: TokenData):
    await delete_on_db(
        collection=WORK,
        criteria={"_id": PydanticObjectId(workId)},
        currentUser=currentUser,
    )


async def edit_work(
    workId: str,
    title: str,
    author: str,
    workType: WorkTypeEnum,
    media: str,
    publicationDate: date,
    publicationProofLink: str,
    currentUser: TokenData,
    publicationProofFile: UploadFile = None,
    authorId: str = None,
):
    publicationDate = datetime.combine(publicationDate, datetime.min.time())
    if publicationProofLink is None:
        publicationProofLink = await upload_publication_proof(publicationProofFile)

    await update_on_db(
        collection=WORK,
        updateData={
            "author": author,
            "title": title,
            "workType": workType,
            "media": media,
            "publicationDate": publicationDate,
            "publicationProof": publicationProofLink,
            "authorId": PydanticObjectId(authorId) if authorId else None,
        },
        currentUser=currentUser,
        criteria={"_id": PydanticObjectId(workId)},
    )
