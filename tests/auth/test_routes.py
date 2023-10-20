import pytest
from httpx import AsyncClient

from src.main import app
from starlette import status

client = AsyncClient(app=app, base_url="http://testserver")


@pytest.mark.asyncio
async def test_login() -> None:
    resp = await client.post(
        "/auth/login",
        json={
            "username": "janedoe",
            "password": "123456",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json["user"]["username"] == "janedoe"


@pytest.mark.asyncio
async def test_refresh_token():
    user_response = await client.post(
        "/auth/login",
        json={
            "username": "janedoe",
            "password": "123456",
        },
    )
    user_response_dict = user_response.json()
    print(user_response_dict)
    refresh_token_response = await client.put("/auth/tokens",
                                              cookies={"refreshToken": user_response_dict["refresh_token"]})
    refresh_token_response_dict = refresh_token_response.json()
    assert refresh_token_response.status_code == status.HTTP_200_OK
    assert user_response_dict["access_token"] == refresh_token_response_dict["access_token"]
    assert user_response_dict["refresh_token"] != refresh_token_response_dict["refresh_token"]
