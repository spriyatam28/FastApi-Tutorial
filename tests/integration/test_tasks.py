import pytest
from httpx import AsyncClient
from fastapi import status

from tests import ROUTE_PREFIX

TASKS_URL: str = f"{ROUTE_PREFIX}/tasks"


@pytest.mark.asyncio
async def test_user_tasks(test_client: AsyncClient, created_task):
    response = await test_client.get(f"{TASKS_URL}/{created_task['user_id']}")

    assert response.status_code == status.HTTP_200_OK

    task_list = response.json()

    assert isinstance(task_list, list)

    task_data = task_list[0]

    assert "id" in task_data

    for k in task_data:
        assert task_data[k] == created_task[k]


@pytest.mark.asyncio
async def test_user_task_by_id(test_client: AsyncClient, created_task):
    response = await test_client.get(f"{TASKS_URL}/{created_task['user_id']}/{created_task['id']}")

    assert response.status_code == status.HTTP_200_OK

    task_data = response.json()

    assert isinstance(task_data, dict)
    assert "id" in task_data

    for k in task_data:
        assert task_data[k] == created_task[k]


@pytest.mark.asyncio
async def test_update_task(test_client: AsyncClient, created_task):
    updated_task_payload = {
        "user_id": created_task["user_id"],
        "id": created_task["id"],
        "task_title": "Updated task...",
        "task_body": "Updated task body",
        "due_date": "2026-02-01",
        "completed": True
    }

    response = await test_client.patch(f"{TASKS_URL}", json=updated_task_payload)

    assert response.status_code == status.HTTP_200_OK

    updated_task_data = response.json()

    assert isinstance(updated_task_data, dict)
    assert "id" in updated_task_data

    for k in updated_task_data:
        if k in updated_task_payload:
            assert updated_task_data.get(k) == updated_task_payload.get(k)


@pytest.mark.asyncio
async def test_delete_task_by_id(test_client: AsyncClient, created_task):
    response = await test_client.delete(f"{TASKS_URL}/{created_task['user_id']}/{created_task['id']}")

    assert response.status_code == status.HTTP_200_OK

    deleted_task_data = response.json()

    assert isinstance(deleted_task_data, dict)
    assert "id" in deleted_task_data

    for k in deleted_task_data:
        if k in created_task:
            assert deleted_task_data[k] == created_task[k]


@pytest.mark.asyncio
async def test_delete_all_user_tasks(test_client: AsyncClient, created_task):
    response = await test_client.delete(f"{TASKS_URL}/{created_task['user_id']}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["successful"] == True
