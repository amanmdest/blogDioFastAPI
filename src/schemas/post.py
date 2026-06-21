from pydantic import AwareDatetime, BaseModel


class PostIn(BaseModel):
    title: str
    content: str
    published_at: AwareDatetime | None = None
    updated_at: AwareDatetime | None = None
    published: bool = True


class PostPut(BaseModel):
    title: str | None = None
    content: str | None = None
    updated_at: AwareDatetime | None = None
    published: bool | None = None
