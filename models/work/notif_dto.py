from pydantic import BaseModel


class OutputCountNotifs(BaseModel):
    count: int
