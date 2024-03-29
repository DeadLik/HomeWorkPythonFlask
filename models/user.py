from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str
    email: str = Field(max_length=128)


class UserIn(BaseModel):
    username: str
    email: str = Field(max_length=128)
    password: str = Field(min_length=6)
