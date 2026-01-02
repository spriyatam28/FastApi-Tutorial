import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database import get_db, Base
from src.main import app
from tests import engine

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
    """Provide a clean database session for each test"""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()  # Rollback any uncommitted changes
        await session.close()


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