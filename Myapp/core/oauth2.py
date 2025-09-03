from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from Myapp import token as tokens
from Myapp import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):  
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn`t validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    return tokens.verify_token(token, credentials_exeption, db)
    
    