import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database import get_db, Base
from src.main import app
from tests import engine, ROUTE_PREFIX

USER_URL = f"{ROUTE_PREFIX}/users"

TestSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ------------------------
# Setup/teardown database tables
# ------------------------
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
    """Create tables before each test, drop after"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ------------------------
# Database session fixture
# ------------------------
@pytest_asyncio.fixture
async def db_session():
    async with engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSession(bind=connection, expire_on_commit=False)

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()


# ------------------------
# FastAPI dependency override
# ------------------------
async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


# ------------------------
# Async test client
# ------------------------
@pytest_asyncio.fixture
async def test_client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        yield client


# ------------------------
# Cleanup on test session end
# ------------------------
@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """Cleanup after all tests complete"""
    yield
    # Dispose of the engine after all tests
    import asyncio

    asyncio.run(engine.dispose())


@pytest.fixture
async def created_user(test_client: AsyncClient):
    payload = {"name": "Test User", "email": "test.user@example.com"}

    response = await test_client.post(f"{USER_URL}", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    user = response.json()

    yield user

    # Delete the user after the test
    await test_client.delete(f"{USER_URL}/{user['id']}")
