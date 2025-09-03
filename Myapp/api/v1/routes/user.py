from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Myapp import schemas
from Myapp import database
from Myapp.core import oauth2
from Myapp.repository import user
from typing import Annotated

get_db = Annotated[Session, Depends(database.get_db)]

public_router = APIRouter(
    prefix="/user",
    tags=['User']
    
)

protected_router = APIRouter(
    prefix="/user",
    tags=['User'],
    dependencies=[Depends(oauth2.get_current_user)]
    
)


#create user
@public_router.post('/', response_model=schemas.UserShow)
def create_user(request: schemas.User, db: get_db):
    return user.create(request, db)

#ger all users
@public_router.get('/', response_model=list[schemas.UserShow])
def get_users(db: get_db):
    return user.get_all(db)

#get user by id
@protected_router.get('/{email}', response_model=schemas.UserShow)
def get_user(email: str, db: get_db):
    return user.get_one(email, db)