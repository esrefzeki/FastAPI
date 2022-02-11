from fastapi import FastAPI
from FastAPI.src.api.infrastructure.persistance.db_manager import engine
from FastAPI.src.api.models import models
from FastAPI.src.routers import post, user, auth
from FastAPI.src.config import GlobalConfig

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
