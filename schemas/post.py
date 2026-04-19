import datetime

from pydantic import BaseModel

dt = datetime.datetime


class PostIn(BaseModel):
    title: str
    date: dt = dt.now(datetime.timezone.utc)
    published: bool = False
    author: str
