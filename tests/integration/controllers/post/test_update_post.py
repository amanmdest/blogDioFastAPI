import pytest
import pytest_asyncio

from httpx import AsyncClient
from fastapi import status 
from fastapi.encoders import isoformat


@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    await service.create(PostIn(title="post 1", content="some content", published=True))
    await service.create(PostIn(title="post 2", content="some content", published=True))
    await service.create(PostIn(title="post 3", content="some content", published=False))


async def test_update_post(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    post_id = 1
    data = {'title': 'post 1 (edited)'}

    response = await client.put(f'/posts/{post_id}', json=data, headers=headers)

    assert response.status_code == status.HTTP_200_OK


async def test_fail_update_post_unauthorized(client: AsyncClient):
    post_id = 1

    response = await client.put(f'/posts/{post_id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_fail_update_post_not_found(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    post_id = 5
    data = {'title': 'post 1 (edited)'}

    response = await client.put(f'/posts/{post_id}', json=data, headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND

