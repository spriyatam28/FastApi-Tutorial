import pytest
from fastapi import status
from httpx import AsyncClient

from tests import ROUTE_PREFIX

BASE_URL = "/users"


@pytest.mark.asyncio
async def test_get_all_users(test_client: AsyncClient):
    payload = {"name": "Test User", "email": "test.user@example.com"}
    create_res = await test_client.post(f"{ROUTE_PREFIX}{BASE_URL}", json=payload)

    assert create_res.status_code == status.HTTP_201_CREATED

    create_data = create_res.json()

    response = await test_client.get(f"{ROUTE_PREFIX + BASE_URL}")

    assert response.status_code == status.HTTP_200_OK

    users = response.json()
    user = users[0]

    assert "id" in user
    assert user["id"] == create_data["id"]
    assert user["name"] == payload["name"]
    assert user["email"] == payload["email"]


@pytest.mark.asyncio
async def test_get_user_by_id(test_client: AsyncClient):
    payload = {"name": "Test User", "email": "test.user1@example.com"}
    create_res = await test_client.post(f"{ROUTE_PREFIX}{BASE_URL}", json=payload)

    assert create_res.status_code == status.HTTP_201_CREATED

    created_user = create_res.json()
    user_id = created_user["id"]

    response = await test_client.get(f"{ROUTE_PREFIX}{BASE_URL}/{user_id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]


@pytest.mark.asyncio
async def test_create_user(test_client: AsyncClient):
    user_payload = {"name": "Test User", "email": "test.user@example.com"}

    response = await test_client.post(f"{ROUTE_PREFIX + BASE_URL}", json=user_payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["name"] == user_payload["name"]
    assert data["email"] == user_payload["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_update_user(test_client: AsyncClient):
    user_payload = {"name": "Test User", "email": "test.user@example.com"}

    created_response = await test_client.post(f"{ROUTE_PREFIX + BASE_URL}", json=user_payload)

    assert created_response.status_code == status.HTTP_201_CREATED

    create_data = created_response.json()

    assert "id" in create_data
    assert create_data["name"] == user_payload["name"]
    assert create_data["email"] == user_payload["email"]

    # Checking if both name and email is updated
    update_payload1 = {"id": create_data["id"], "name": "Test User Both", "email": "test.user.both@example.com"}

    updated_response = await test_client.patch(f"{ROUTE_PREFIX + BASE_URL}", json=update_payload1)

    assert updated_response.status_code == status.HTTP_201_CREATED

    updated_data1 = updated_response.json()

    assert "id" in updated_data1
    assert updated_data1["id"] == create_data["id"]
    assert updated_data1["email"] == update_payload1["email"]
    assert updated_data1["name"] == update_payload1["name"]

    # Checking if only name is updated
    update_payload2 = {"id": create_data["id"], "name": "Test User Name"}

    updated_response = await test_client.patch(f"{ROUTE_PREFIX + BASE_URL}", json=update_payload2)

    assert updated_response.status_code == status.HTTP_201_CREATED

    updated_data2 = updated_response.json()

    assert "id" in updated_data2
    assert updated_data2["id"] == create_data["id"]
    assert updated_data2["email"] == updated_data1["email"]
    assert updated_data2["name"] == update_payload2["name"]

    # Checking if only email is updated
    update_payload3 = {"id": create_data["id"], "email": "test.user.email@example.com"}

    updated_response = await test_client.patch(f"{ROUTE_PREFIX + BASE_URL}", json=update_payload3)

    assert updated_response.status_code == status.HTTP_201_CREATED

    updated_data3 = updated_response.json()

    assert "id" in updated_data3
    assert updated_data3["id"] == create_data["id"]
    assert updated_data3["email"] == update_payload3["email"]
    assert updated_data3["name"] == updated_data2["name"]


@pytest.mark.asyncio
async def test_delete_user(test_client: AsyncClient):
    user_payload = {"name": "Test User", "email": "test.user@example.com"}

    created_response = await test_client.post(f"{ROUTE_PREFIX + BASE_URL}", json=user_payload)

    assert created_response.status_code == status.HTTP_201_CREATED

    create_data = created_response.json()

    assert "id" in create_data
    assert create_data["name"] == user_payload["name"]
    assert create_data["email"] == user_payload["email"]

    deleted_response = await test_client.delete(f"{ROUTE_PREFIX + BASE_URL}/{create_data['id']}")

    assert deleted_response.status_code == status.HTTP_200_OK

    data = deleted_response.json()

    assert "id" in data
    assert data["id"] == create_data["id"]
    assert data["name"] == create_data["name"]
    assert data["email"] == create_data["email"]
