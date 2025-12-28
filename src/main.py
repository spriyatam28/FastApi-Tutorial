from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from src.storage.database import Base, engine, get_db
from src.task.task_dao import create_task, update_task
from src.task.task_model import TaskCreate, Task, TaskUpdate
from src.user.user_dao import create_new_user
from src.user.user_model import User, UserCreate

app=FastAPI(
    title="FastAPI tutorial",
    debug=True,
    description="Learning how to build backend systems using FastAPI",
    version="0.1.0",
    contact={
        "author":"spriyatam28"
    }
)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return "Hello, World!!!"

@app.get("/task/{user_id}")
async def get_tasks(user_id:int, db:Session=Depends(get_db)):
    tasks=db.query(Task).filter(Task.user_id==user_id).all()

    return tasks

@app.post("/task/{user_id}")
async def add_task(user_id:int, task:TaskCreate, db: Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist!!!")

    return create_task(db, user_id, task)

@app.patch("/task/{user_id}/{task_id}")
async def update_user_task(user_id:int, task_id:int, new_task:TaskUpdate, db:Session=Depends(get_db)):
    updated_task=update_task(db, user_id, task_id, new_task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found!!!")

    return updated_task


@app.post("/user")
async def create_user(user:UserCreate, db: Session=Depends(get_db)):
    if db.query(User).filter(User.email==user.email).first():
        raise HTTPException(status_code=404, detail="Email already exists. Try with another email!")

    return create_new_user(db, user)

@app.get("/user")
async def get_users(db:Session=Depends(get_db)):
    users=db.query(User).all()

    return users