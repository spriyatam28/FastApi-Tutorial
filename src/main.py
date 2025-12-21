from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from src.storage.storage import Base, engine, get_db
from src.task.task_dao import create_task
from src.task.task_model import TaskCreate
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

@app.post("/task/{user_id}")
async def add_task(user_id:int, task:TaskCreate, db: Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found!!!")

    return create_task(db, user_id, task.task_title)

@app.post("/user")
async def create_user(user:UserCreate, db: Session=Depends(get_db)):
    if db.query(User).filter(User.email==user.email).first():
        raise HTTPException(status_code=404, detail="Email already exists. Try with another email!")

    return create_new_user(db, user)

@app.get("/user")
async def get_users(db:Session=Depends(get_db)):
    users=db.query(User).all()

    return users