from pydantic import BaseModel
from datetime import datetime


class TagBase(BaseModel):
    name: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class TagGet(TagBase):
    id: str


class TagUpdate(TagBase):
    name: str | None = None
