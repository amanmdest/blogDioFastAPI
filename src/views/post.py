from pydantic import AwareDatetime, BaseModel


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    updated_at: AwareDatetime | None
    published_at: AwareDatetime | None


class PostUpdated(BaseModel):
    id: int
    title: str
    content: str
    updated_at: AwareDatetime | None
