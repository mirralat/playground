from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class ValidUser(BaseModel):
    id: UUID
    name: str = Field(description='user name')
    password: str = Field(description='password')
    picture: bytes = Field(default=None, description='avatar')
