import datetime

from pydantic import BaseModel

dt = datetime.datetime


class PostOut(BaseModel):
    title: str
    date: dt