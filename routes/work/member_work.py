from fastapi import APIRouter, Depends

from controllers.auth.member import get_current_user_member
from models.authentication.authentication import TokenData
from models.work.work_dto import InputAddWork

route_member_work = APIRouter(
    prefix="/member/work",
    tags=["Member Work"],
    responses={404: {"description": "Not found"}},
)


@route_member_work.post("")
async def member_add_work(
    input: InputAddWork, currentUser: TokenData = Depends(get_current_user_member)
):
    print("current user", currentUser)


@route_member_work.get("")
async def member_get_list_work(
    currentUser: TokenData = Depends(get_current_user_member),
):
    pass
