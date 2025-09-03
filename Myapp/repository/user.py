from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from Myapp import schemas, models
from Myapp.core.hashing import Hash


def get_all(db: Session):
    users = db.query(models.User).all()
    return users

def get_one(email, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="This user not exist")
    
    return user
    

def create(request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already taken")
    
    new_user = models.User(**request.model_dump(exclude={"password"}), password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
    