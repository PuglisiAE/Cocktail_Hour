from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])


class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8)])
    dob =  DateField('Date of Birth', format = '%m/%d/%y', validators=[DataRequired()])
    accept_rules = BooleanField('I am over 21', validators=[InputRequired()])