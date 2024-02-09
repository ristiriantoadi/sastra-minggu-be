from datetime import date

from fastapi import APIRouter, Depends, File, Form, UploadFile

from controllers.auth.member import get_current_user_member
from controllers.work.work_crud import (
    find_works,
    insert_work_to_db,
    validate_publication_proof,
)
from models.authentication.authentication import TokenData
from models.default.base import PaginationDir
from models.work.work_dto import OutputGetListWorks
from models.work.work_enum import WorkTypeEnum

route_member_work = APIRouter(
    prefix="/member/work",
    tags=["Member Work"],
    responses={404: {"description": "Not found"}},
)


@route_member_work.post("")
async def member_add_work(
    title: str = Form(...),
    author: str = Form(...),
    workType: WorkTypeEnum = Form(...),
    media: str = Form(...),
    publicationDate: date = Form(...),
    publicationProofLink: str = Form(None),
    publicationProofFile: UploadFile = File(None),
    currentUser: TokenData = Depends(get_current_user_member),
):
    validate_publication_proof(link=publicationProofLink, file=publicationProofFile)
    await insert_work_to_db(
        title=title,
        author=author,
        workType=workType,
        media=media,
        publicationDate=publicationDate,
        publicationProof=publicationProofLink,
    )
    return "OK"


@route_member_work.get("", response_model=OutputGetListWorks)
async def member_get_list_work(
    dir: PaginationDir,
    page: int,
    sortBy: str = "createTime",
    size: int = 10,
    currentUser: TokenData = Depends(get_current_user_member),
):
    data = await find_works(sortBy=sortBy, page=page, size=size, dir=dir)
    return OutputGetListWorks(
        size=size,
        page=page,
        totalElements=data.totalElements,
        totalPages=data.totalPages,
        sortBy=sortBy,
        sortDir=dir,
        content=data.content,
    )
