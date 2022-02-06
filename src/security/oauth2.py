from jose import JWTError, jwt
from datetime import datetime, timedelta
from FastAPI.src.api.models.dto import token_dto
from FastAPI.src.api.models import models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from FastAPI.src import db_manager
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algoritm
# Expriation time

SECRET_KEY = "09saw7eq9q6f51vf6g8h4w6936gh13hn7r7re856eq1f6sb1as63ax1b6f51hs6v"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = token_dto.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db_manager.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return token