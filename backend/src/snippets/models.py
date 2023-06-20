from pydantic import BaseModel
from datetime import datetime


class SnippetBase(BaseModel):
    title: str
    description: str
    content: str
    language_id: str
    user_email: str
    tags_id: set[str] = set()
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class SnippetGet(SnippetBase):
    id: str


class SnippetUpdate(SnippetBase):
    title: str | None = None
    description: str | None = None
    content: str | None = None
    language_id: str | None = None
    user_email: str | None = None
    tags_id: set[str] | None = None
