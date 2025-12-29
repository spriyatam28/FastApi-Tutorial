from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://spriyatam28:Siva.123@localhost/tasks_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_seesion = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with async_seesion() as session:
        yield session
