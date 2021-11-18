from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Cocktail, Notes, Saved, UserCocktail
from forms import LoginForm, AddUserForm, SearchByNameForm, SearchByIngredientForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from methods import get_random_cocktail, get_cocktails_by_ingredient_name, get_cocktails_by_name



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost:5433/cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "s0m3_s3cRe7_K8Y"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
login_manager = LoginManager()

connect_db(app)

login = LoginManager(app)
login.login_view="home"
cocktails_url = "http://www.thecocktaildb.com/api/json/v1/1/"


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    """Display homepage"""

    return render_template('base.html')


@app.route("/login", methods = ["GET", "POST"])
def login():
    """Handle User Login"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(request.form['username'], request.form['password'])
        if user:
            """log in user & redirect to user home page"""
            login_user(user)
            return redirect(f"users/{user.id}")
        else:
            """error handling for invalid credentials"""
            flash("Invalid email or password", "danger")
            return redirect(url_for('login'))
            
    return render_template('login.html', form=form)

@app.route("/drinks/<letter>", methods = ["GET"])
def by_letter(letter):
    return render_template('drinks_list')


@app.route("/logout", methods = ["POST"])
def logout():
    """logs out user"""
    logout_user()
    return redirect(url_for('home'))




@app.route('/signup', methods=["GET", "POST"])
def signup():
    """handles user signup."""
    form = AddUserForm()

    if form.validate_on_submit():
        """create a new user"""
        user = User.register(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data, 
            dob = form.dob.data)
        print("*******", form.email.data)
        db.session.add(user)

        try:
            db.session.commit()
            login_user(user)
            return redirect(f"users/{user.id}")

        except IntegrityError:
            """handles create user errors if username already taken"""
            flash(f"Username {form.username.data} has already been taken. Please try again.", 'danger')
            return redirect(url_for('signup'))
    else:
        """display user sign-up form"""
        return render_template('add_user.html', form=form)




@app.route("/users/<int:user_id>", methods = ["POST", "GET"])
def user_home(user_id):
    """display use homepage"""
    return render_template('user_home.html')


@app.route("/random", methods = ['GET', 'POST'])
def get_random():
    """get a random cocktail"""
    cocktail = get_random_cocktail(cocktails_url)
    return render_template("display_cocktail.html", cocktail=cocktail)


@app.route("/search/name/", methods = ["GET", "POST"])
def search_byname():
    """search for a cocktail by name"""
    form = SearchByNameForm()
    
    
    if form.validate_on_submit():
        name = form.name.data
        cocktail = get_cocktails_by_name(cocktails_url, name)
        return render_template("display_cocktail.html", cocktail=cocktail)
    else:
        return render_template('search.html', form=form)


@app.route("/search/ingredient/", methods = ["GET", "POST"])
def search_byingredient():
    """search for cocktails by ingredient name"""
    form = SearchByIngredientForm()
    
    if form.validate_on_submit():
        ingredient = form.ingredient.data
        cocktail = get_cocktails_by_ingredient_name(cocktails_url, ingredient)
        return render_template("drinks_list.html", drinks=cocktail)

    else:
        return render_template('search.html', form=form)


@app.route("/search/name/<name>/", methods = ["GET"])
def retrieve_drink(name):
    """retrieve drink by name"""
    cocktail = get_cocktails_by_name(cocktails_url, name)
    return render_template("display_cocktail.html", cocktail=cocktail)
