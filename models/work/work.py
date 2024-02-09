from datetime import datetime

from models.default.base import DefaultModel
from models.work.work_enum import WorkTypeEnum


class Work(DefaultModel):
    title: str
    author: str
    workType: WorkTypeEnum
    media: str
    publicationDate: datetime
    publicationProof: str
