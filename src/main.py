from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from src.api.v1.api import api_router
from src.database import Base, engine, get_db

app = FastAPI(
    title="FastAPI tutorial",
    debug=True,
    description="Learning how to build backend systems using FastAPI",
    version="0.1.0",
    contact={
        "author": "spriyatam28"
    }
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return "Hello, World!!!"
