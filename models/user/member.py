
from models.default.base import DefaultModel
from models.user.user import Credential


class Member(DefaultModel):
    username: str
    credential: Credential
    name: str
