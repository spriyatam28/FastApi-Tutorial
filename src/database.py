import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")

engine = create_async_engine(DB_URI, echo=False, future=True)

async_session = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
	async with async_session() as session:
		yield session
