from typing import List

from fastapi import APIRouter, Depends

from controllers.auth.member import get_current_user_member
from controllers.combo.member_combo import find_all_members
from models.authentication.authentication import TokenData
from models.combo.combo_member import OutputComboMember

route_member_combo = APIRouter(
    prefix="/member/combo",
    tags=["Member Combo"],
    responses={404: {"description": "Not found"}},
)


@route_member_combo.get("", response_model=List[OutputComboMember])
async def member_get_combo_members(
    name: str = "",
    currentUser: TokenData = Depends(get_current_user_member),
):
    members = await find_all_members(name)
    return members
