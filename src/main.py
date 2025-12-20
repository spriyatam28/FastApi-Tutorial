from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from src.storage.storage import Base, engine, get_db
from src.task.task_dao import create_task
from src.task.task_model import TaskCreate
from src.user.user_model import User

app=FastAPI(
    title="FastAPI tutorial",
    debug=True,
    description="Learning how to build backend systems using FastAPI",
    version="0.1.0",
    contact={
        "name":"Priyatam",
        "email":"spriyatam28.work@gmail.com",
        "twitter":"https://x.com/vnp268"
    }
)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return "Hello, World!!!"

@app.post("/task/{user_id:int}")
async def add_task(user_id:int, task:TaskCreate, db: Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found!!!")

    return create_task(db, user_id, task.task_title)