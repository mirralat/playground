from pydantic import BaseModel, Field


class ValidUser(BaseModel):
    name: str = Field(..., description='user name')
    password: str = Field(..., description='password')
    avatar: bytes = Field(..., default=None, description='avatar')
