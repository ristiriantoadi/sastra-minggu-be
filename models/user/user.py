from enum import Enum

from pydantic import BaseModel


class UserTypeEnum(str, Enum):
    MEMBER = "MEMBER"


class Credential(BaseModel):
    password: str
