from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# Algoritm
# Expriation time

SECRET_KEY = "09saw7eq9q6f51vf6g8h4w6936gh13hn7r7re856eq1f6sb1as63ax1b6f51hs6v"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
