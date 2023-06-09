from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(200))
    permissions = db.Column(db.Integer)


class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    shortName = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    price = db.Column(db.Float)
    promotion = db.Column(db.Boolean, default=False)
    dueDate = db.Column(db.DateTime, nullable=True)


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    shortName = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    url = db.Column(db.String(200))
    date = db.Column(db.DateTime)
