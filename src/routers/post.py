import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from fastapi.params import Body
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from FastAPI.src.db_manager import engine, get_db
from FastAPI.src.api.models import models
from FastAPI.src.security import utility, oauth2
from sqlalchemy.orm import Session
from FastAPI.src.api.models.dto import post_crud, users_dto
from FastAPI.src.routers import post, user


router = APIRouter(
    prefix="/posts",
    tags=["Posts API"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_crud.PostResponse)
def create_posts(post: post_crud.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # 1:
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    # RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # 2:
    # new_post = models.Post(title=post.title,
    #                        content=post.content,
    #                        published=post.published)

    new_post = models.Post(owner_id=current_user.id, **post.dict()) # **post.dict() ile istenen düm içerik inputlarını saymış oluyoruz.

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=post_crud.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    the_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not the_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")

    return the_post


@router.get("/", response_model=List[post_crud.PostResponse], )
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()
    return posts


@router.put("/{id}")
def update_post(id: int, post: post_crud.PostBase,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")

    if post.id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    post_delete = db.query(models.Post).filter(models.Post.id == id)
    deleted = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")

    post_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)