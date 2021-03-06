from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



# models go below

class User(db.Model, UserMixin):
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
    email = db.Column(db.Text, nullable=False, unique=True
    ) 
    dob = db.Column(db.DateTime, nullable=False)
    saved_cocktails = db.relationship('Cocktail', secondary = "saved_cocktails", backref = "user")
    user_cocktails = db.relationship('UserCocktail', backref = 'user')
    


    def saved_cocktail(self, cocktail):

        self.saved.append(cocktail)
        db.session.commit()

    @classmethod
    def register(cls, username, password, email, dob):
        """Register new user with a hashed password, and return the user"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username = username, password = hashed_pwd, email = email, dob = dob)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exists and password is valid"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class Cocktail(db.Model):
    """cocktails info"""

    __tablename__="cocktails"

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(80), nullable = False, unique=True)
    drink_img_url = db.Column(db.String(), nullable = True)


class Saved(db.Model):

    """Info about saved cocktails"""

    __tablename__ = "saved_cocktails"

    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id', ondelete = "CASCADE"), primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = "CASCADE"), primary_key = True)


class UserCocktail(db.Model):
    """User created cocktail"""

    __tablename__ = "user_cocktails"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(80), nullable = False)
    instructions = db.Column(db.String(), nullable = False)
    alcoholic = db.Column(db.String(), nullable = False)
    glass = db.Column(db.String(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = "CASCADE"))
    drink_img_url = db.Column(db.String(), nullable = True)
    recipe = db.relationship('UserCocktailIngredient', backref = 'user_cocktails', cascade = "all, delete-orphan")


class UserCocktailIngredient(db.Model):
    """user created ingredients for user_cocktails"""

    __tablename__ = "user_cocktail_ingredients"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('user_cocktails.id', ondelete="CASCADE"))
    name = db.Column(db.String(), nullable = False)
    amount = db.Column(db.Float(), nullable = False)
    measurement = db.Column(db.String(), nullable = False)




