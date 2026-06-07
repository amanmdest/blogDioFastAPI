from fastapi import status
from fastapi.encoders import isoformat
from httpx import AsyncClient


async def test_create_post_success(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'title': 'post 1', 
        'content': 'some content', 
        'published': True
    }
    response = await client.post('/posts/', json=data, headers=headers)
    content = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert content['id'] is not None


async def test_fail_create_post_invalid_payload(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'content': 'some content', 
        'published': True
    }
    response = await client.post('/posts/', json=data, headers=headers)
    content = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert content['detail'][0]['loc'] == ['body', 'title']


async def test_fail_create_post_unauthorized(client: AsyncClient):
    data = {
        'title': 'post 2', 
        'content': 'some content', 
        'published': True
    }
    response = await client.post('/posts/', json=data, headers={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED