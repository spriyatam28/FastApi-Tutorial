from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine

ROUTE_PREFIX = "/api/v1"

TEST_DB_URL = "postgresql+asyncpg://spriyatam28:Siva.123@localhost:5432/test_tasks_db"

engine = create_async_engine(TEST_DB_URL, future=True, echo=False, poolclass=NullPool)
