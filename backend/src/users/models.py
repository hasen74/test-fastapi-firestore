from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class UserGet(UserBase):
    id: str


class UserUpdate(UserBase):
    email: str | None = None
#     first_name: str | None = None
#     last_name: str | None = None


# class Token(BaseModel):
#     token: str
