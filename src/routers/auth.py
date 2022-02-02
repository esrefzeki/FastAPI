from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from FastAPI.src.db_manager import get_db
from FastAPI.src.security import utility, oauth2
from FastAPI.src.api.models.dto import users_dto
from FastAPI.src.api.models import models
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utility.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    access_token = oauth2.create_access_token()
