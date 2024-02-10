from datetime import date

from fastapi import APIRouter

from controllers.work.work_crud import find_works, get_filter_list_work
from models.default.base import PaginationDir
from models.work.work_dto import OutputGetListWorks
from models.work.work_enum import WorkTypeEnum

route_guest_work = APIRouter(
    prefix="/guest/work",
    tags=["Guest Work"],
    responses={404: {"description": "Not found"}},
)


@route_guest_work.get("", response_model=OutputGetListWorks)
async def guest_get_list_work(
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
    return OutputGetListWorks(
        size=size,
        page=page,
        totalElements=data.totalElements,
        totalPages=data.totalPages,
        sortBy=sort,
        sortDir=dir,
        content=data.content,
    )
