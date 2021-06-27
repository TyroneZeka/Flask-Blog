from enum import unique
from db import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

class Category(db.Model,Base):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(255), nullable = False,unique = True)
    short_desc = db.Column(db.Text())
    posts = db.relationship("Posts",lazy=True)

    def __init__(self,post_id,category,desc) -> None:
        self.post_id = post_id
        self.category = category
        self.short_desc = desc
        super().__init__()