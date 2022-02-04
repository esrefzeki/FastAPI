from datetime import time
import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from fastapi.params import Body
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from FastAPI.src.db_manager import engine, get_db
from FastAPI.src.api.models import models
from FastAPI.src.security import utility
from sqlalchemy.orm import Session
from FastAPI.src.api.models.dto import post_crud, users_dto
from FastAPI.src.routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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
