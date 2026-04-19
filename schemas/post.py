import datetime

from pydantic import BaseModel

dt = datetime.datetime


class PostIn(BaseModel):
    title: str
    author: str
    date: dt = dt.now(datetime.timezone.utc)
    published: bool = True
