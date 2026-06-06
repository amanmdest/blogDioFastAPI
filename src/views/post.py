import datetime

from pydantic import BaseModel

dt = datetime.datetime


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    updated_at: dt | None
    published_at: dt | None


class PostUpdated(BaseModel):
    id: int
    title: str
    content: str
    updated_at: dt | None
