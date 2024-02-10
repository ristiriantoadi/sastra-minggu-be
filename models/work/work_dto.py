from datetime import date, datetime
from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from models.default.base import DefaultPage


class DataOutputGetListWork(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    createTime: datetime
    title: str
    author: str
    workType: str
    media: str
    publicationDate: date
    publicationProof: str


class OutputGetListWorks(DefaultPage):
    content: List[DataOutputGetListWork]


class DataOutputGetListWorkPrivate(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    createTime: datetime
    creatorId: PydanticObjectId
    title: str
    author: str
    workType: str
    media: str
    publicationDate: date
    publicationProof: str
    isEditable: bool = False


class OutputGetListWorksPrivate(DefaultPage):
    content: List[DataOutputGetListWorkPrivate]
