from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# models go below

class User(db.Model):
    """users info"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(25),
                     nullable=False,
                     unique=True)
    password = db.Column(db.Text, nullable=False,
    )
    email = db.Column(db.Text, nullable=False, unique=True,
    )
    dob = db.Column(db.String(8), nullable=False)
    notes = db.relationship('Notes', backref = "user")
    saved = db.relationship('Saved', backref = "user")


class Cocktail(db.Model):
    """cocktails info"""

    __tablename__="beers"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(80), nullable = False, unique=True)
    drink_img_url = db.Column(db.String(), nullable = True)


class Notes(db.Model):
    """Info about user notes"""

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktail.id'), primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)


class Saved(db.Model):

    """Info about saved beers"""

    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktail.id'), primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)


class UserCocktail(db.Model):
    """User created cocktail"""

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(80), nullable = False)
    ingredients = db.Column(db.String(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)


  
