from pydantic import BaseModel
from datetime import datetime


class SnippetBase(BaseModel):
    title: str
    description: str
    content: str
    language_id: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class SnippetUpdate(SnippetBase):
    title: str | None = None
    description: str | None = None
    content: str | None = None
    language_id: str | None = None
