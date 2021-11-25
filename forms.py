from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DateField, SelectField, widgets, SelectMultipleField
from datetime import datetime
from wtforms.validators import DataRequired, Length, InputRequired, Email
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


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CreateDrinkForm(FlaskForm):
    """Form for creating a drink from ingredient list"""

    ingredients = MultiCheckboxField('Ingredients', coerce=str)
    




  


