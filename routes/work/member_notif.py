from fastapi import APIRouter, Depends

from controllers.auth.member import get_current_user_member
from controllers.work.notif import get_notif_counts, reset_notif_counts
from models.authentication.authentication import TokenData
from models.work.notif_dto import OutputCountNotifs

route_member_notif = APIRouter(
    prefix="/member/notif",
    tags=["Member Notif"],
    responses={404: {"description": "Not found"}},
)


@route_member_notif.get("/count", response_model=OutputCountNotifs)
async def member_get_count_notifs(
    currentUser: TokenData = Depends(get_current_user_member),
):
    count = await get_notif_counts(currentUser)
    return {"count": count}


@route_member_notif.get("/reset_count")
async def member_reset_count_notifs(
    currentUser: TokenData = Depends(get_current_user_member),
):
    await reset_notif_counts(currentUser)
    return "OK"
