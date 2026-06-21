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


@pytest.mark.parametrize('published, total', [('true', 2), ('false', 1)] )
async def test_read_posts_by_status_success(client: AsyncClient, access_token:str, 
                                            published: str, total: int):
    params = {'published': published, 'limit': total}
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get('/posts/', params=params, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == total


@pytest.mark.parametrize('published, wrong_total', [('true', 1), ('false', 2)] )
async def test_read_posts_by_status_wrong_total(client: AsyncClient, access_token:str,
                                           published: str, wrong_total: int):
    params = {'published': published, 'limit': 10}
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get('/posts/', params=params, headers=headers)

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) != wrong_total


async def test_read_posts_limit_success(client: AsyncClient, access_token: str):
    params = {"published": "on", "limit": 1}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 1


async def test_read_posts_empty_parameters_fail(client: AsyncClient, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/posts/", params={}, headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_fail_read_posts_unauthorized(client: AsyncClient):
    response = await client.get('/posts/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED