from datetime import date

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, File, Form, UploadFile

from controllers.auth.member import get_current_user_member
from controllers.work.work_crud import (
    add_additional_data_works,
    delete_work,
    find_works,
    get_filter_list_work,
    insert_work_to_db,
    validate_publication_proof_must_exist,
)
from models.authentication.authentication import TokenData
from models.default.base import PaginationDir
from models.work.work_dto import OutputGetListWorks, OutputGetListWorksPrivate
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
    authorId: str = Form(None),
    currentUser: TokenData = Depends(get_current_user_member),
):
    validate_publication_proof_must_exist(
        link=publicationProofLink, file=publicationProofFile
    )
    await insert_work_to_db(
        title=title,
        author=author,
        workType=workType,
        media=media,
        publicationDate=publicationDate,
        publicationProofLink=publicationProofLink,
        publicationProofFile=publicationProofFile,
        currentUser=currentUser,
        authorId=authorId,
    )
    return "OK"


@route_member_work.get("", response_model=OutputGetListWorksPrivate)
async def member_get_list_work(
    title: str = None,
    author: str = None,
    workType: WorkTypeEnum = None,
    media: str = None,
    startDate: date = None,
    endDate: date = None,
    dir: PaginationDir = PaginationDir.DESC,
    page: int = 0,
    sort: str = "createTime",
    size: int = 10,
    currentUser: TokenData = Depends(get_current_user_member),
):
    data = await find_works(
        sort=sort,
        page=page,
        size=size,
        dir=dir,
        criteria=get_filter_list_work(
            title=title,
            author=author,
            workType=workType,
            media=media,
            startDate=startDate,
            endDate=endDate,
        ),
    )
    data.content = add_additional_data_works(data=data.content, currentUser=currentUser)
    return OutputGetListWorksPrivate(
        size=size,
        page=page,
        totalElements=data.totalElements,
        totalPages=data.totalPages,
        sortBy=sort,
        sortDir=dir,
        content=data.content,
    )


@route_member_work.delete("/{workId}")
async def member_delete_work(
    workId: str,
    currentUser: TokenData = Depends(get_current_user_member),
):
    await delete_work(workId=workId, currentUser=currentUser)
    return "OK"


@route_member_work.get("/my_work", response_model=OutputGetListWorks)
async def member_get_my_work(
    dir: PaginationDir = PaginationDir.DESC,
    page: int = 0,
    sort: str = "createTime",
    size: int = 10,
    currentUser: TokenData = Depends(get_current_user_member),
):
    data = await find_works(
        size=size,
        page=page,
        sort=sort,
        dir=dir,
        criteria={"authorId": PydanticObjectId(currentUser.userId)},
    )
    return OutputGetListWorks(
        size=size,
        page=page,
        totalElements=data.totalElements,
        totalPages=data.totalPages,
        sortBy=sort,
        sortDir=dir,
        content=data.content,
    )
