from fastapi import FastAPI
from FastAPI.src.api.infrastructure.persistance.db_manager import engine
from FastAPI.src.api.models import models
from FastAPI.src.routers import post, user, auth, votes
from FastAPI.src import config
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware

# AŞAĞIDAKİ yoruma alınmış kod satırı sqlalchmey ile db'nin güncellenmesi sağlanıyordu fakat alembic'ten ötürü gerek kalmadı.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["https://www.google.com", "https://www.icmimarlikdergisi.com"]
origins = ["*"] # Herkesin erişmesi için

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def get_settings():
    return config.GlobalConfig()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
