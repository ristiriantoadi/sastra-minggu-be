
from pydantic import BaseModel


class InputAddWork(BaseModel):
    title: str
    author: str
