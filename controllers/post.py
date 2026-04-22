import datetime

from fastapi import APIRouter, status
from schemas.post import PostIn, PostPut
from services.post import PostService
from views.post import PostOut, PostUpdated

dt = datetime.datetime
router = APIRouter(prefix='/posts')
services = PostService()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    return await services.create(post)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[PostOut])
async def read_posts(published: bool = True, limit: int = 10, skip: int = 0):
    return await services.read_all(limit, skip, published)


@router.get('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostOut)
async def read_post_by_id(post_id: int):
    return await services.read(post_id)


@router.put('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostUpdated)
async def update_post(post: PostPut, post_id: int):
    return await services.update(post, post_id)


@router.delete('/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(post_id: int):
    return await services.delete(post_id)
