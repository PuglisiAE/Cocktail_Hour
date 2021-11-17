from flask import Flask, request, render_template, redirect, flash, session, login
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from forms import LoginForm, AddUserForm

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost:5433/cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "s0m3_s3cRe7_K8Y"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
login_manager = LoginManager(app)

connect_db(app)


@app.route("/login", methods = ["Post"])
def home_page():
    """Handle User Login"""
    form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup. Create new user and add to DB. Redirect to home page.
    If form not valid, present form. If the there already is a user with that username: flash message and re-present form.
    """
    form = AddUserForm()

