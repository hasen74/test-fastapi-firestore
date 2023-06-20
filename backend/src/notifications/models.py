from pydantic import BaseModel
from datetime import datetime


class NotificationBase(BaseModel):
    content: str
    snippet_id: str
    user_email: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class NotificationGet(NotificationBase):
    id: str


class NotificationUpdate(NotificationBase):
    content: str | None = None
    snippet_id: str | None = None
    user_email: str | None = None
