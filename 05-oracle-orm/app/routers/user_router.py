import logging
from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
import app.services.user_service as user_service
from app.schemas.user import UserCreate, UserOut, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["User"])

@router.get(
        "/", 
        response_description=List[UserOut], 
        summary="Get all users",
        description="Fetch a list of all users with pagination support using `skip` and `limit`."
)
def fetch_all_users(skip:int=0, limit:int=100, db:Session = Depends(get_db)):
    logger.info("All users are retrieved successfully")
    return user_service.get_all_users(db, skip=skip, limit=limit)

@router.get(
        "/{user_id}", 
        response_model=UserOut,
        summary="Get user by ID",
        description="Fetch a specific user by their unique `user_id`."
)
def get_user_by_id(user_id:int, db:Session = Depends(get_db)):
    db_user = user_service.get_user_by_id(db, user_id)
    if not db_user:
        logger.warn("User id {user_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    logger.info(f"User with {user_id} retrieved successfully")
    return db_user

@router.post(
        "/", 
        response_model=UserOut,
        status_code=status.HTTP_201_CREATED,
        summary="Create new user",
        description="Add a new user to the database. All fields are optional except `name`."
)
def create_user(user_in:UserCreate, db:Session = Depends(get_db)):
    return user_service.create_user(db, user_in)

@router.put(
        "/{user_id}", 
        response_model=UserOut,
        summary="Update existing user",
        description="Update details of an existing user by providing their `user_id` and updated fields."
)
def update_user(user_id:int, user_in:UserUpdate, db:Session = Depends(get_db)):
    updated_user = user_service.update_user(db, user_id, user_in)
    if not updated_user:
        logger.warn("User id {user_id} not found for updating from the database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

@router.delete(
        "/{user_id}", 
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete user",
        description="Delete a user permanently from the database using their `user_id`."
)
def delete_user(user_id:int, db:Session = Depends(get_db)):
    ok = user_service.delete_user(db, user_id)
    if not ok:
        logger.warn("User id {user_id} not found for removing from database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None