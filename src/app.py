import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
from FastAPI.src.db_manager import engine, get_db
from FastAPI.src.api.models import models
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts }

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[str] = None


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


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db())):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    # RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    models.Post(title=post.title,
                content=post.content,
                published=post.published)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return post


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")

    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict

    return {'data': post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")
    return {"info": f"The post which has id {id} removed."}
