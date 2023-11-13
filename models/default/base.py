from datetime import datetime
from typing import Any, List

from beanie import PydanticObjectId
from pydantic import BaseModel


class DefaultModel(BaseModel):
    createTime: datetime
    creatorId: PydanticObjectId

    updateTime: datetime = None
    updaterId: PydanticObjectId = None

    deleteTime: datetime = None
    deleterId: PydanticObjectId = None
    isDelete: bool = False


class DefaultPage(BaseModel):
    # status: int = 200
    size: int = 0
    page: int = 0
    totalElements: int = 0
    totalPages: int = 0
    sortBy: str
    sortDir: int
    content: List[Any] = []
