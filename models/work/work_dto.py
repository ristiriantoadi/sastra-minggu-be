from datetime import date
from typing import List

from pydantic import BaseModel

from models.default.base import DefaultPage


class DataOutputGetListWork(BaseModel):
    title: str
    author: str
    workType: str
    media: str
    publicationDate: date
    publicationProof: str


class OutputGetListWorks(DefaultPage):
    content: List[DataOutputGetListWork]
