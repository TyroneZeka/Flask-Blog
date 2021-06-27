from sqlalchemy.orm import relationship
from db import db
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Posts(db.Model,Base):
    __tablename__= 'posts'

    id = db.Column(db.Integer,primary_key = True)
    author = db.Column(db.String(80))
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    summary = db.Column(db.Text())
    createdAt = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    updatedAt = db.Column(db.DateTime())
    publishedAt = db.Column(db.DateTime())
    slug = db.Column(db.String(255),unique=True)
    content = db.Column(db.Text())
    comments = db.relationship("Comments", backref="post_comment", lazy=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship("Category",viewonly=True)

    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'))
    tags = db.relationship("Tags",viewonly=True)

    def __init__(self,authorId,title,subtitle,summary,updatedAt,publishedAt,content) -> None:
        super().__init__()
        self.authorId = authorId
        self.title = title
        self.subtitle = subtitle 
        self.summary=summary
        self.updatedAt = updatedAt
        self.publishedAt = publishedAt
        self.content = content

