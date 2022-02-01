import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from fastapi.params import Body
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from FastAPI.src.db_manager import engine, get_db
from FastAPI.src.api.models import models
from FastAPI.src.security import utility
from sqlalchemy.orm import Session
from FastAPI.src.api.models.dto import users_dto
from FastAPI.src.routers import post, user

router = APIRouter(
    prefix="/user",
    tags=["Users API"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=users_dto.UserResponse)
def create_posts(user: users_dto.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=users_dto.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} does not exist.")

    return user


@router.get("/", response_model=List[users_dto.UserResponse])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    deleted_user = db.query(models.User).filter(models.User.id == id).first()

    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} does not exist.")

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)