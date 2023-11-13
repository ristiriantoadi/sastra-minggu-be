from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth.member import authenticate_member, create_token_for_member
from models.authentication.auth_dto import InputRegistration

route_guest_auth = APIRouter(
    prefix="/guest/auth",
    tags=["Guest auth"],
    responses={404: {"description": "Not found"}},
)


@route_guest_auth.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    member = await authenticate_member(
        username=form_data.username, password=form_data.password
    )
    access_token = create_token_for_member(member)
    return {"access_token": access_token, "token_type": "bearer"}


@route_guest_auth.post("/register")
async def register(input: InputRegistration):
    pass
