from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.api import api_router
from src.database import Base, engine

@asynccontextmanager
async def lifespan():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(
    title="FastAPI tutorial",
    debug=True,
    description="Learning how to build backend systems using FastAPI",
    version="0.1.0",
    contact={
        "author": "spriyatam28"
    }
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return "Hello, World!!!"
