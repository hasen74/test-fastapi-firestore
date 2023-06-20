from pydantic import BaseModel
from datetime import datetime


class LanguageBase(BaseModel):
    name: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class LanguageGet(LanguageBase):
    id: str


class LanguageUpdate(LanguageBase):
    name: str | None = None
