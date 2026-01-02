import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.api import api_router
from src.core.exception_handlers import app_exception_handler
from src.core.exceptions import AppException
from src.database import Base, engine

ENV = os.getenv("ENV", "development")
API_PREFIX = "/api/v1"

docs_url = None if ENV == "production" else "/docs"
redoc_url = None if ENV == "production" else "/redoc"
openapi_url = None if ENV == "production" else "/openapi.json"


@asynccontextmanager
async def lifespan():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

	yield

	await engine.dispose()


app = FastAPI(
	title="FastAPI tutorial",
	debug=None if ENV == "production" else True,
	docs_url=docs_url,
	redoc_url=redoc_url,
	openapi_url=openapi_url,
	description="Learning how to build backend systems using FastAPI",
	version="0.1.0",
	contact=None if ENV == "production" else {"name": "spriyatam28", "url": "https://github.com/spriyatam28/FastApi-Tutorial"},
	license_info={
		"name": "GPL v3",
		"url": "https://github.com/spriyatam28/FastApi-Tutorial/blob/main/LICENSE",
	},
)

app.include_router(api_router, prefix=API_PREFIX)
app.add_exception_handler(AppException, app_exception_handler)


@app.get("/")
async def root():
	return {"msg": True}


@app.get("/health")
async def check_health():
	return {"msg": "Working!!!"}
