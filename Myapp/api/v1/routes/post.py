from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Myapp import schemas, database
from Myapp.services.post_service import PostService
from Myapp.repository import post
from Myapp.core import oauth2
from typing import Annotated, Optional
import sys


get_db = Annotated[Session, Depends(database.get_db)]
current_user = Annotated[schemas.UserShow, Depends(oauth2.get_current_user)]
filter = Annotated[schemas.PaginationFilter, Depends()]

public_router = APIRouter(
    prefix="/post",
    tags=['Post']
)

protected_router = APIRouter(
    prefix="/post",
    tags=['Post'],
    dependencies=[Depends(oauth2.get_current_user)]
)

#Get the all posts
@public_router.get('/', response_model=schemas.PagingationResponse[schemas.PostShow])
def get_posts(db: get_db, filter: filter):
    service = PostService(db)
    return service.get_all_posts(filter)

@public_router.get('/by-username/{username}', response_model=list[schemas.PostShow])
def get_posts_by_username(username: str, db: get_db):
    print(username)
    service = PostService(db)
    posts = service.get_posts_by_username(username)
    
    return posts

#Get the single post
@protected_router.get('/{id}', response_model=schemas.PostShow)
def get_post(id, db: get_db):
    return post.get_one(id, db)
    
#Create new post
@protected_router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Post, db : get_db, current_user: current_user):
    print(current_user)
    return post.create(request, db, current_user)

#Update post
@protected_router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Post, db: get_db, current_user: current_user):
    return post.update(id, request, db, current_user)
    
#Delete post
@protected_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: get_db, current_user: current_user):
    return post.destroy(id, db, current_user)


