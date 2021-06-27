from db import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

class Tags(db.Model,Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key = True)
    tag = db.Column(db.String(80))
    posts = db.relationship("Posts",lazy=True)

    def __init__(self,post_id,tag) -> None:
        self.post_id = post_id
        self.tag = tag
        super().__init__()
    