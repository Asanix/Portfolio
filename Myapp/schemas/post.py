from pydantic import BaseModel
from typing import Optional
from . import UserShow


class Post(BaseModel):
    title: str
    description: str

class PostShow(BaseModel):
    id: int
    title: str
    description: str
    creator: UserShow
    
    class Config():
        orm_mode = True