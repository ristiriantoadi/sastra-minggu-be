from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth.authentication import PWDCONTEXT
from controllers.auth.member import authenticate_member, create_token_for_member
from controllers.member.member_crud import find_member_on_db, insert_member_to_db
from models.authentication.auth_dto import InputRegistration
from models.user.member import Member

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
    member = await find_member_on_db({"username": input.username})
    if member:
        raise HTTPException(status_code=400, detail="Username sudah dipakai")
    member = Member(
        username=input.username,
        name=input.name,
        credential={"password": PWDCONTEXT.encrypt(input.password)},
    )
    await insert_member_to_db(member)
    return "OK"
