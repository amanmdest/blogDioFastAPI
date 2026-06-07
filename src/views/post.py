# from pydantic import AwareDatetime, BaseModel


# class PostOut(BaseModel):
#     id: int
#     title: str
#     content: str
#     updated_at: AwareDatetime | None
#     published_at: AwareDatetime | None


# class PostUpdated(BaseModel):
#     id: int
#     title: str
#     content: str
#     updated_at: AwareDatetime | None

from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, field_validator

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: datetime | None = None
    updated_at: datetime | None = None
    published: bool

    # This fixes SQLite by automatically attaching UTC if the DB returned it as naive
    @field_validator('published_at', 'updated_at', mode='before')
    @classmethod
    def ensure_timezone(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

class PostUpdated(PostOut):
    pass