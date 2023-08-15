from pydantic import BaseModel, Field, Extra, PrivateAttr
from uuid import UUID, uuid4


class ValidUser(BaseModel):
    id: UUID
    name: str = Field(description='user name')
    password: str = Field(description='password')
    picture: bytes = Field(None, description='avatar')
    _User__isAdmin: bool = PrivateAttr(default=False)
