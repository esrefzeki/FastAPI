import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
from FastAPI.src.db_manager import engine, get_db
from FastAPI.src.api.models import models
from sqlalchemy.orm import Session
from FastAPI.src.api.models.dto import post_crud


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='18351989',
                               cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=post_crud.PostResponse)
def create_posts(post: post_crud.PostCreate, db: Session = Depends(get_db)):
    # 1:
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    # RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # 2:
    # new_post = models.Post(title=post.title,
    #                        content=post.content,
    #                        published=post.published)

    new_post = models.Post(**post.dict()) # **post.dict() ile istenen düm içerik inputlarını saymış oluyoruz.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}", response_model=post_crud.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    the_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not the_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")

    return the_post


@app.get("/posts", response_model=List[post_crud.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.put("/posts/{id}")
def update_post(id: int, post: post_crud.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    check_it = post_query.first()

    if check_it == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return {'data': post_query.first()}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
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
    # message = "The item has been removed."

    return Response(status_code=status.HTTP_204_NO_CONTENT)
