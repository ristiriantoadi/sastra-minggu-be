from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from controllers.auth.member import get_current_user_member
from controllers.member.member_crud import find_member_on_db
from models.authentication.auth_dto import OutputCheckToken
from models.authentication.authentication import TokenData

route_member_auth = APIRouter(
    prefix="/member/auth",
    tags=["Member auth"],
    responses={404: {"description": "Not found"}},
)


@route_member_auth.post("/check_token", response_model=OutputCheckToken)
async def check_token(current_user: TokenData = Depends(get_current_user_member)):
    member = await find_member_on_db({"_id": PydanticObjectId(current_user.userId)})
    return member
