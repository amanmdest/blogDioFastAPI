from databases.interfaces import Record
from fastapi import HTTPException, status

from database import database
from models.post import posts
from schemas.post import PostIn, PostPut


class PostService:
    async def create(self, post: PostIn) -> None:
        command = posts.insert().values(
            title=post.title, 
            content=post.content,
            published_at=post.published_at,
            updated_at=post.updated_at,
            published=post.published,
        )
        return await database.execute(command)


    async def read_all(self, limit: int, skip: int, published: bool) -> list[Record]:
        query = posts.select().limit(limit).offset(skip)
        return await database.fetch_all(query)


    async def read(self, post_id: int) -> Record:
        return await self.__get_by_id(post_id)


    async def update(self, post: PostPut, post_id: int) -> Record:
        total = await self.count(post_id)       
        if not total:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Post Not Found'
            )

        data = post.model_dump(exclude_unset=True)
        command = posts.update().where(posts.c.id == post_id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(post_id)

    
    async def delete(self, post_id: int) -> None:
        command = posts.delete().where(posts.c.id == post_id)
        await database.execute(command)
    

    async def count(self, post_id: int) -> int:
        query = "select count(id) as total from posts where id = :post_id"
        result = await database.fetch_one(query, {"id": post_id})
        return result.total
    

    async def __get_by_id(self, post_id) -> Record:
        query = posts.select().where(posts.c.id == post_id)
        post = await database.fetch_one(query)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return post
