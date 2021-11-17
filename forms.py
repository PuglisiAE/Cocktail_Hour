from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DateField
from datetime import datetime
from wtforms.validators import DataRequired, Length, Email, InputRequired


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
    