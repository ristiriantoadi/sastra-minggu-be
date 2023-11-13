from fastapi import APIRouter

route_guest_work = APIRouter(
    prefix="/guest/work",
    tags=["Guest Work"],
    responses={404: {"description": "Not found"}},
)


@route_guest_work.get("")
async def guest_get_list_work():
    pass
