from sqlalchemy.orm import relationship
from db import db
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comments(db.Model,Base):
    id = db.Column(db.Integer, primary_key = True)
    publishedOn = db.Column(db.DateTime(),nullable =False, default=datetime.datetime.utcnow) 
    content = db.Column(db.Text(), nullable = False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)
    post = relationship("Posts",viewonly=True)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    user = relationship("UserModel", viewonly=True)

    def __init__(self,content,publishedOn,post_id,user_id) -> None:
        self.content = content
        self.publishedOn = publishedOn
        self.post_id = post_id
        self.user_id = user_id
        super().__init__()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()