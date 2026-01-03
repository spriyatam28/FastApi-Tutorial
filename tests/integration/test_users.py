import pytest
from fastapi import status
from httpx import AsyncClient

from tests import ROUTE_PREFIX

USER_URL: str = f"{ROUTE_PREFIX}/users"


@pytest.mark.asyncio
async def test_get_all_users(test_client: AsyncClient, created_user):
    response = await test_client.get(f"{USER_URL}")

    assert response.status_code == status.HTTP_200_OK

    users = response.json()
    user = users[0]

    assert "id" in user
    assert user["id"] == created_user["id"]
    assert user["name"] == created_user["name"]
    assert user["email"] == created_user["email"]


@pytest.mark.asyncio
async def test_user_by_id(test_client: AsyncClient, created_user):
    response = await test_client.get(f"{USER_URL}/{created_user['id']}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == created_user


@pytest.mark.asyncio
async def test_update_user(test_client: AsyncClient, created_user):
    # Checking if both name and email is updated
    update_payload1 = {"id": created_user['id'], "name": "Test User Both", "email": "test.user.both@example.com"}

    updated_response = await test_client.patch(f"{USER_URL}", json=update_payload1)

    assert updated_response.status_code == status.HTTP_201_CREATED

    updated_data1 = updated_response.json()

    assert "id" in updated_data1
    assert updated_data1["id"] == created_user["id"]
    assert updated_data1["email"] == update_payload1["email"]
    assert updated_data1["name"] == update_payload1["name"]

    # Checking if only name is updated
    update_payload2 = {"id": created_user['id'], "name": "Test User Name"}

    updated_response = await test_client.patch(f"{USER_URL}", json=update_payload2)

    assert updated_response.status_code == status.HTTP_201_CREATED

    updated_data2 = updated_response.json()

    assert "id" in updated_data2
    assert updated_data2["id"] == created_user['id']
    assert updated_data2["email"] == updated_data1["email"]
    assert updated_data2["name"] == update_payload2["name"]

    # Checking if only email is updated
    update_payload3 = {"id": created_user['id'], "email": "test.user.email@example.com"}

    updated_response = await test_client.patch(f"{USER_URL}", json=update_payload3)

    assert updated_response.status_code == status.HTTP_201_CREATED

    updated_data3 = updated_response.json()

    assert "id" in updated_data3
    assert updated_data3["id"] == created_user['id']
    assert updated_data3["email"] == update_payload3["email"]
    assert updated_data3["name"] == updated_data2["name"]


@pytest.mark.asyncio
async def test_delete_user(test_client: AsyncClient, created_user):
    deleted_response = await test_client.delete(f"{USER_URL}/{created_user['id']}")

    assert deleted_response.status_code == status.HTTP_200_OK

    data = deleted_response.json()

    assert "id" in data
    assert data["id"] == created_user['id']
    assert data["name"] == created_user["name"]
    assert data["email"] == created_user["email"]
