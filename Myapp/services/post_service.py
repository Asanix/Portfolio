from sqlalchemy.orm import Session
from Myapp.repository.post import get_all, get_posts_by_username
from Myapp.models import Post, User
from Myapp.schemas import PaginationFilter

class PostService():
    def __init__(self, db: Session):
        self.db = db
        
    def get_all_posts(self, filter: PaginationFilter):
        post = get_all(self.db, filter)
        
        return post
    
    def get_posts_by_username(self, username: str):
        return get_posts_by_username(self.db, username)
        