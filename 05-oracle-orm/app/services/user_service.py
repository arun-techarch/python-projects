import logging
from app.models.user import User
from typing import Optional, List
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate

logger = logging.getLogger(__name__)

def get_all_users(db:Session, skip:int = 0, limit:int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db:Session, user_id:int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db:Session, user_in:UserCreate) -> User:
    db_user = User(**user_in.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f'User {db_user.name} entry was created successfully')
    return db_user

def update_user(db:Session, user_id:int, user_in:UserUpdate) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f'User {db_user.name} entry was updated successfully')
    return db_user

def delete_user(db:Session, user_id:int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    logger.info(f'User {db_user.name} entry was removed successfully')
    return True