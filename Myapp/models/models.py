from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from Myapp.database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category_name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
        
    creator = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    
    
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    
    posts = relationship("Post", back_populates="creator")
    categories = relationship("Category", back_populates="user")
    
    __table_args__ = (
        Index('idx_username', 'username', unique=True),
        Index('idx_email', 'email', unique=True),
    )
    
    
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    
    user = relationship("User", back_populates="categories")
    posts = relationship("Post", back_populates="category")
    
    __table_args__ = (
        Index('idx_name', 'name', unique=True),
    )
    