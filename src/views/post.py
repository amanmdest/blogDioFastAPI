from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    updated_at: AwareDatetime | NaiveDatetime | None
    published_at: AwareDatetime | NaiveDatetime | None


class PostUpdated(BaseModel):
    id: int
    title: str
    content: str
    updated_at: AwareDatetime | NaiveDatetime | None
