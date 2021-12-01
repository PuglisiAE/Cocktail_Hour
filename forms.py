from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DateField, SelectField, widgets, SelectMultipleField, Form, FloatField, BooleanField
from datetime import datetime
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange
from api_helper import CocktailDetails


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), InputRequired()])


class AddUserForm(FlaskForm):
    """Form for adding user"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8)])
    dob =  DateField('Date of Birth', format = '%Y-%m-%d', default=datetime.now(), validators=[InputRequired()])

class EditUserForm(FlaskForm):
    """Form for editing user"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Check-Password', validators=[Length(min=8)])
    dob =  DateField('Date of Birth', format = '%Y-%m-%d', default=datetime.now(), validators=[InputRequired()])
        




    
class SearchByNameForm(FlaskForm):
    """Form for searching by name"""

    name = StringField('Drink Name', validators = [DataRequired()])

class SearchByIngredientForm(FlaskForm):
    """Form for searching by Ingredient"""

    ingredient = SelectField('Ingredient', choices = CocktailDetails.get_all_ingredients(), validators = [DataRequired()])


class IngredientForm(FlaskForm):
    name = StringField('Ingredient', validators = [DataRequired()])
    amount = FloatField('Amount', validators = [DataRequired(message = "Must be a valid number")])
    measurement = SelectField('Measurement', choices = ["cubes", "cup", "cl", "dash", "drop", "gal", "garnish", "l", "ml", "oz", "part", "pint", "shot", "sprig", "Tbsp", "tsp", "wedge", "whole"])

class CreateDrinkForm(FlaskForm):
    name = StringField('Cocktail Name')
    instructions = TextAreaField('Instructions')
    alcoholic = SelectField('Alcoholic', choices = ["Alcoholic", "Non-Alcoholic"], validators = [DataRequired()])
    glass = StringField('Glass Type')
    drink_img_url = StringField('Drink Image URL')
    








  


