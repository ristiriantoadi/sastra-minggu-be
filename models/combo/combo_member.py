from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class OutputComboMember(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str
    username: str
