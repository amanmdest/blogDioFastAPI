from datetime import datetime, timezone

import sqlalchemy as sa

from databases.interfaces import Record

from src.database import database
from src.exceptions import NotFoundPostError
from src.models.post import posts
from src.schemas.post import PostIn, PostPut


class PostService:
    async def create(self, post: PostIn) -> None:
        # Fallback to current timezone-aware time if None is provided
        published_at = post.published_at or datetime.now(timezone.utc)
        updated_at = post.updated_at or datetime.now(timezone.utc)

        # print("PUBLISHED_AT TZINFO:", published_at.tzinfo)
        # print("UPDATED_AT TZINFO:", updated_at.tzinfo)

        command = posts.insert().values(
            title=post.title, 
            content=post.content,
            published_at=published_at,
            updated_at=updated_at,
            published=post.published,
        )
        return await database.execute(command)


    async def read_all(self, limit: int, skip: int, published: bool) -> list[Record]:
        query = posts.select().limit(limit).offset(skip)
        return await database.fetch_all(query)


    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)


    async def update(self, post: PostPut, id: int) -> Record:
        total = await self.count(id)       
        if not total:
            raise NotFoundPostError

        data = post.model_dump(exclude_unset=True)

        # Force updated_at to be explicitly timezone-aware on every update
        data["updated_at"] = datetime.now(timezone.utc)

        command = posts.update().where(posts.c.id == id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(id)

    
    async def delete(self, id: int) -> None:
        command = posts.delete().where(posts.c.id == id)
        await database.execute(command)
    

    async def count(self, id: int) -> int:
        # query = "select count(id) as total from posts where id = :id"
        # result = await database.fetch_one(query, {"id": id})

        # Using SQLAlchemy Core to generate the count query safely
        query = sa.select(sa.func.count(posts.c.id)).where(posts.c.id == id)
        result = await database.execute(query)  # returns the count integer directly
        return result
    

    async def __get_by_id(self, id: int) -> Record:
        query = posts.select().where(posts.c.id == id)
        post = await database.fetch_one(query)
        if not post:
            raise NotFoundPostError
        return post
