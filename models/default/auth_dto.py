from pydantic import BaseModel


class OutputCheckToken(BaseModel):
    name: str
    noId: str
