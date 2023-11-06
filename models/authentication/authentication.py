from datetime import datetime

from pydantic import BaseModel


class TokenData(BaseModel):
    userId: str
    exp: datetime
