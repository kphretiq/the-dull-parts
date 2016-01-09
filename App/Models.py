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
