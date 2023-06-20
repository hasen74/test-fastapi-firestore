from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    snippet_id: str
    user_email: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class CommentGet(CommentBase):
    id: str


class CommentUpdate(CommentBase):
    content: str | None = None
    snippet_id: str | None = None
    user_email: str | None = None
