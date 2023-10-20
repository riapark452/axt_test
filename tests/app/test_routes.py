import datetime
import random

import pytest
import pytest_asyncio
from httpx import AsyncClient
from starlette import status

from src.auth import jwt
from src.main import app

client = AsyncClient(app=app, base_url="http://testserver")


@pytest_asyncio.fixture
async def access_token():
    access_token = jwt.create_access_token(user={"id": 1, "username": "janedoe", "is_admin": 1, "password": "123456"})
    return access_token


@pytest.mark.asyncio
async def test_create():
    start_date = datetime.datetime(1990, 1, 1)
    num = random.randint(100000, 20000000)
    step = datetime.timedelta(seconds=num)
    birthdate = (start_date + step).strftime('%Y-%m-%d')
    response = await client.post("/users/create",
                                 json={
                                     "username": f"testuser_{num}",
                                     "password": "123456",
                                     "name": "Test User",
                                     "birthdate": birthdate,
                                     "is_admin": 0,
                                     "is_online": 1
                                 })
    response_dict = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_dict['username'] == f"testuser_{num}"
    assert response_dict['birthdate'] == birthdate


@pytest.mark.asyncio
async def test_create_fail():
    num = random.randint(100000, 20000000)

    response = await client.post("/users/create",
                                 json={
                                     "username": f"testuser_{num}",
                                     "password": "123456",
                                     "name": "Test User",
                                     "is_admin": 0,
                                     "is_online": 1
                                 })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_list(access_token: str):
    response = await client.get("/users/list/all", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_detail(access_token: str):
    response = await client.get("/users/get/1", headers={"Authorization": f"Bearer {access_token}"})
    response_dict = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_dict["username"] == "janedoe"


@pytest.mark.asyncio
async def test_detail_fail(access_token: str):
    response = await client.get("/users/get/100000", headers={"Authorization": f"Bearer {access_token}"})
    response_dict = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response_dict["msg"] == "User not found"


@pytest.mark.asyncio
async def test_create_username_taken():
    start_date = datetime.datetime(1990, 1, 1)
    num = random.randint(100000, 20000000)
    step = datetime.timedelta(seconds=num)
    birthdate = (start_date + step).strftime('%Y-%m-%d')
    response = await client.post("/users/create",
                                 json={
                                     "username": "janedoe",
                                     "password": "123456",
                                     "name": "Test User",
                                     "birthdate": birthdate,
                                     "is_admin": 0,
                                     "is_online": 1
                                 })

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_update(access_token: str):
    response = await client.put("/users/update/1", headers={"Authorization": f"Bearer {access_token}"}, json={
        "name": "Updated name",
        "birthdate": "1990-01-01",
        "is_admin": 1,
        "is_online": 1
    })
    response_dict = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_dict["name"] == "Updated name"
    assert response_dict["is_admin"] == 1


@pytest.mark.asyncio
async def test_update_fail(access_token: str):
    response = await client.put("/users/update/100000", headers={"Authorization": f"Bearer {access_token}"}, json={
        "name": "Updated name",
        "birthdate": "1990-01-01",
        "is_admin": 1,
        "is_online": 0
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete(access_token: str):
    response = await client.delete("/users/delete/1006", headers={"Authorization": f"Bearer {access_token}"})
    response_dict = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_dict["msg"] == "Successful deletion" or "Record with this id doesn't exist"
