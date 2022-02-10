from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from FastAPI.src.config import GlobalConfig
from psycopg2.extras import RealDictCursor
import psycopg2
from datetime import time


SQLALCHEMY_DATABASE_URL = f"postgresql://{GlobalConfig.DB_USERNAME}:{GlobalConfig.DB_PASSWORD}@{GlobalConfig.DB_HOST}/{GlobalConfig.DB_NAME}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
