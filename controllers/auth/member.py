from fastapi import Depends, HTTPException

from controllers.auth.authentication import (
    PWDCONTEXT,
    create_token,
    get_current_user,
    oauth2_scheme_member,
)
from controllers.member.member_crud import find_member_on_db


def get_current_user_member(token: str = Depends(oauth2_scheme_member)):
    return get_current_user(token)


def create_token_for_member(member: dict):
    return create_token(member)


async def authenticate_member(username: str, password: str):
    member = await find_member_on_db(criteria={"username": username.strip()})
    if member is None:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    if not PWDCONTEXT.verify(password.strip(), member["credential"]["password"]):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    return member
