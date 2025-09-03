from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from Myapp import schemas, models


def get_posts_by_username(db: Session, username):
    return db.query(models.Post).join(models.User).filter(models.User.username == username).all()

def get_all(db: Session, filter: schemas.PaginationFilter):
    skip = (filter.page - 1) * filter.limit
    query = db.query(models.Post)
    
    posts = query.offset(skip).limit(filter.limit).all()
    total = query.count()
    return {
        "data": posts,
        "total": total,
        "page": filter.page,
        "limit": filter.limit,
        "pages": (total + filter.limit - 1) // filter.limit 
    }

def get_one(id, db: Session):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post


def create(request: schemas.Post, db: Session, current_user):
    new_post = models.Post(**request.model_dump(), user_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update(id, request: schemas.Post, db: Session, current_user):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post not found")
    
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    
    post.update(request.model_dump())
    db.commit()
    return post.first()

def destroy(id, db: Session, current_user):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post not found")
    
    if delete_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    
    delete_post.delete(synchronize_session=False)
    db.commit()
    return "done"
    