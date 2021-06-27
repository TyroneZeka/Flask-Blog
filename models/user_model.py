from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
    
class UserModel(UserMixin,db.Model,Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(45))
    email = db.Column(db.String(50), unique=True)
    passwordHash = db.Column(db.String(80))
    registeredAt = db.Column(db.DateTime())
    is_admin = db.Column(db.Boolean,default=False)
    comments = db.relationship("Comments",backref = "user_comment", lazy = True)
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, firstName, lastName,email,passwordHash,registeredAt,is_admin) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.passwordHash = passwordHash
        self.registeredAt = registeredAt
        self.is_admin = is_admin

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)