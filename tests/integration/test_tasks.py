import pytest
from httpx import AsyncClient

from tests import ROUTE_PREFIX

TASKS_URL: str = f"{ROUTE_PREFIX}/tasks"


@pytest.mark.asyncio
async def test_user_tasks(test_client: AsyncClient):
	pass


@pytest.mark.asyncio
async def test_user_task_by_id(test_client: AsyncClient):
	pass


@pytest.mark.asyncio
async def test_create_task(test_client: AsyncClient):
	pass


@pytest.mark.asyncio
async def test_update_task(test_client: AsyncClient):
	pass


@pytest.mark.asyncio
async def test_delete_task_by_id(test_client: AsyncClient):
	pass


@pytest.mark.asyncio
async def test_delete_all_user_tasks(test_client: AsyncClient):
	pass
