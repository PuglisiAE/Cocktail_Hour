from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DateField
from datetime import datetime
from wtforms.validators import DataRequired, Length, InputRequired, Email


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), InputRequired()])


class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8)])
    dob =  DateField('Date of Birth', format = '%Y-%m-%d', default=datetime.now(), validators=[InputRequired()])
    
class SearchByNameForm(FlaskForm):
    """Form for searching by name"""

    name = StringField('Drink Name', validators = [DataRequired()])

class SearchByIngredientForm(FlaskForm):
    """Form for searching by Ingredient"""

    ingredient = StringField('Ingredient', validators = [DataRequired()])




  


