import datetime

from pydantic import BaseModel

dt = datetime.datetime


class PostIn(BaseModel):
    title: str
    content: str
    published_at: dt | None = None
    updated_at: dt | None = None
    published: bool = False


class PostPut(BaseModel):
    title: str | None = None
    content: str | None = None
    updated_at: dt | None = None
    published: bool | None = None
