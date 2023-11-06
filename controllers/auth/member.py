from datetime import datetime, timedelta

import jwt
from beanie import PydanticObjectId
from fastapi import Depends, HTTPException
from jose import JWTError

from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from controllers.util.authentication import oauth2_scheme_member
from models.authentication.authentication import TokenData


def get_current_user_member(token: str = Depends(oauth2_scheme_member)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tokenData = TokenData(
            userId=payload.get("userId"),
            exp=payload.get("exp"),
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Token tidak valid")

    return tokenData


def create_token_for_member(member: dict):
    data = TokenData(
        userId=str(member["_id"]),
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    encoded_jwt = jwt.encode(data.dict(), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_member(username: str, password: str):
    return {"_id": PydanticObjectId()}
