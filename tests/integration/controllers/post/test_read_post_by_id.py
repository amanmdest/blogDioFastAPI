import pytest
import pytest_asyncio

from httpx import AsyncClient
from fastapi import status


@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    await service.create(PostIn(title="post 1", content="some content", published=True))
    await service.create(PostIn(title="post 2", content="some content", published=True))
    await service.create(PostIn(title="post 3", content="some content", published=False))


async def test_read_post_by_id(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    post_id = 1

    response = await client.get(f'/posts/{post_id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == post_id


async def test_fail_read_post_by_id_not_found(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    post_id = 5

    response = await client.get(f'/posts/{post_id}', headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_fail_read_post_by_id_unauthorized(client: AsyncClient):
    post_id = 1

    response = await client.get(f'/posts/{post_id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
