from pydantic import BaseModel


class InputRegistration(BaseModel):
    username: str
    password: str
    name: str
