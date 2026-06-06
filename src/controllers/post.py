import datetime

from fastapi import APIRouter, Depends, status
from src.schemas.post import PostIn, PostPut
from src.security import login_required
from src.services.post import PostService
from src.views.post import PostOut, PostUpdated

dt = datetime.datetime

router = APIRouter(prefix='/posts', tags=["posts"], dependencies=[Depends(login_required)])

services = PostService()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    # return await services.create(post)
    return {**post.model_dump(), "id": await services.create(post)}


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[PostOut])
async def read_posts(published: bool, limit: int = 10, skip: int = 0):
    return await services.read_all(limit, skip, published)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostOut)
async def read_post_by_id(id: int):
    return await services.read(id)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PostUpdated)
async def update_post(post: PostPut, id: int):
    return await services.update(post, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    return await services.delete(id)
