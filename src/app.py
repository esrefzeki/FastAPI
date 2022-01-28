import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
# from FastAPI.src.db_manager import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)

my_post = [{"title": "title of the content - 1", "content": "content of the post - 1", "id": 1},
           {"title": "title of the content - 2", "content": "content of the post - 2", "id": 2}]


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
def create_posts(post: Post):
    cursor.e
    my_post.append(post_dict)
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
