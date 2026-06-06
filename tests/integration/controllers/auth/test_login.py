from fastapi import status
from httpx import AsyncClient


async def test_login_success(client: AsyncClient):
    # Given - fornecer de entrada
    data = {"user_id": 1}

    # When - ação do teste
    response = await client.post('/auth/login', json=data)

    # Then - conclusão
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['access_token'] is not None
