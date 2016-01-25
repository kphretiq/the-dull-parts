# -*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import SQLAlchemy
from flaskext.auth.models.sa import get_user_class

db = SQLAlchemy()

# authentication User class from flask-auth
User = get_user_class(db.Model)

class Profile(db.Model):
    __tablename__ = "profile"
    __searchable__ = ["username", "email", "first_name", "last_name"]

    id = db.Column(db.Integer, primary_key = True)
    # yes, this is redundant. Live with it.
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(254))
    first_name = db.Column(db.String(255))
    middle = db.Column(db.String(1))
    last_name = db.Column(db.String(255))
    street = db.Column(db.String(255))
    street2 = db.Column(db.String(255))
    country = db.Column(db.String(3))
    subdivision = db.Column(db.String(6))
    city = db.Column(db.String(32))
    postal_code = db.Column(db.String(12))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="profile")

class TempAuth(db.Model):
    __tablename__ = "temp_auth"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(254))
    key = db.Column(db.String(254))
    stamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# TODO: check out using "after_delete" event to remove media
# http://docs.sqlalchemy.org/en/latest/orm/events.html
class Page(db.Model):
    """
    "children" is Adjacency List:
        http://docs.sqlalchemy.org/en/latest/orm/self_referential.html
    """
    __tablename__ = "page"
    __searchable__ = ["name",]

    id = db.Column(db.Integer, primary_key = True)
    parent_id = db.Column(db.Integer, db.ForeignKey("page.id"))
    name = db.Column(db.String(255), unique=True, nullable=False)
    blurb = db.Column(db.String(255))
    content = db.Column(db.Text) # expect markdown
    role = db.Column(db.Enum("default", "primary", "featured"), default="default") 
    disabled = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    children = db.relationship("Page",
            backref=db.backref("parent", remote_side=[id])
            )
    media = db.relationship("Media", backref="page", lazy="dynamic")

# TODO: check out using "after_delete" event to trigger removal of media from s3
class Media(db.Model):
    __tablename__ = "media"
    __searchable__ = []

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    uri = db.Column(db.String(255), unique=True, nullable=False)
    mime_type = db.Column(db.String(24))
    alt = db.Column(db.String(255), nullable=False) # alt tag string here
    page_id = db.Column(db.Integer, db.ForeignKey("page.id"))
