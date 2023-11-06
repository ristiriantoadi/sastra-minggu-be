from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth.member import authenticate_member, create_token_for_member

route_member_auth = APIRouter(
    prefix="/member/auth",
    tags=["Member auth"],
    responses={404: {"description": "Not found"}},
)


@route_member_auth.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    member = await authenticate_member(
        username=form_data.username, password=form_data.password
    )
    access_token = create_token_for_member(member)
    return {"access_token": access_token, "token_type": "bearer"}
