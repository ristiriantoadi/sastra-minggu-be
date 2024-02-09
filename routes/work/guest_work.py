from fastapi import APIRouter

from controllers.work.work_crud import find_works
from models.default.base import PaginationDir
from models.work.work_dto import OutputGetListWorks

route_guest_work = APIRouter(
    prefix="/guest/work",
    tags=["Guest Work"],
    responses={404: {"description": "Not found"}},
)


@route_guest_work.get("")
async def guest_get_list_work(
    dir: PaginationDir,
    page: int = 0,
    sort: str = "createTime",
    size: int = 10,
):
    data = await find_works(sort=sort, page=page, size=size, dir=dir, criteria={})
    return OutputGetListWorks(
        size=size,
        page=page,
        totalElements=data.totalElements,
        totalPages=data.totalPages,
        sortBy=sort,
        sortDir=dir,
        content=data.content,
    )
