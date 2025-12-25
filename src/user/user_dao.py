from sqlalchemy.orm import Session

from src.user.user_model import User, UserCreate


def create_new_user(db: Session, user: UserCreate):
    new_user=User(name=user.name, email=user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user