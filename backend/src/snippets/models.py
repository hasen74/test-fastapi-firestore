from pydantic import BaseModel
from datetime import datetime


class SnippetCreate(BaseModel):
    title: str
    description: str
    content: str
    language_id: str
    user_email: str
    createdAt: datetime = datetime.utcnow()


class SnippetUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    content: str | None = None
    language_id: str | None = None
    user_email: str | None = None
    updatedAt: datetime = datetime.utcnow()
