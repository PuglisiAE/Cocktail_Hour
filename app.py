from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Cocktail, Notes, Saved, UserCocktail
from forms import LoginForm, AddUserForm, SearchByNameForm, SearchByIngredientForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from api_helper import CocktailDetails, cocktails_url
import string



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



@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def welcome():
    """Display welcome/login/signup links"""
    
    return render_template("welcome.html")


@app.route("/home/<int:user_id>")
@login_required
def home(user_id):
    """Display homepage"""
    current_user = User.query.get_or_404(user_id)
    return render_template('home.html', current_user=current_user)


@app.route("/login", methods = ["GET", "POST"])
def login():
    """Handle User Login"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(request.form['username'], request.form['password'])
        if user:
            """log in user & redirect to user home page"""
            login_user(user)
            return redirect(f"/user/{user.id}")
        else:
            """error handling for invalid credentials"""
            flash("Invalid email or password", "danger")
            return redirect(url_for('login'))
            
    return render_template('login.html', form=form)

@app.route("/drinks/<letter>", methods = ["GET"])
def by_letter(letter):
    return render_template('drinks_list.html')


@app.route("/logout/<int:user_id>", methods = ["GET", "POST"])
def logout(user_id):
    """logs out user"""
    if current_user.id != user_id:
        flash("You do not have permission to see this page", "danger")
        return redirect(f"/user/{current_user.id}")
    else: 
        user = User.query.get_or_404(user_id)
        logout_user()
        return redirect(url_for("welcome"))


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
            return redirect(f"/home/{user.id}")

        except IntegrityError:
            """handles create user errors if username already taken"""
            flash(f"Username {form.username.data} has already been taken. Please try again.", 'danger')
            return redirect(url_for('signup'))
    else:
        """display user sign-up form"""
        return render_template('add_user.html', form=form)




@app.route("/user/<int:user_id>", methods = ["POST", "GET"])
@login_required
def user_home(user_id):
    """display use homepage"""
    if current_user.id != user_id:
        flash("You do not have permission to see this page", "danger")
        return redirect(f"/user/{current_user.id}")
    
    else: 
        return render_template('user_home.html', user=current_user)


@app.route("/random", methods = ['GET', 'POST'])
@login_required
def get_random():
    """get a random cocktail"""
    cocktail = CocktailDetails.get_random_cocktail(cocktails_url)
    return render_template("display_cocktail.html", cocktail=cocktail)



@app.route("/search/name/<name>/", methods = ["GET"])
@login_required
def search_name(name):
    """retrieve drink by name"""
    cocktails = CocktailDetails.get_cocktails_by_name(name)
    return render_template("drinks_list.html", drinks=cocktails)



@app.route("/search/ingredient/<ingredient>/", methods = ["GET"])
@login_required
def search_ing(ingredient):
    """retrieve drink by name"""
    cocktail = CocktailDetails.get_cocktails_by_ingredient_name(ingredient)
    return render_template("display_cocktail.html", cocktail=cocktail)



@app.route("/search/<first_letter>", methods = ["GET", "POST"])
@login_required
def search_by_letter(first_letter):
    """gets drinks by first letter"""
    cocktail = CocktailDetails.get_cocktails_by_first_letter(first_letter)
    return render_template(
             "drinks_list.html", drinks = cocktail)


@app.route("/search", methods=['GET'])
@login_required
def search():
    """handles user searches"""
    name_form = SearchByNameForm()
    ingredient_form = SearchByIngredientForm()
    range = list(string.ascii_uppercase)

    return render_template('search.html', name_form = name_form, ingredient_form = ingredient_form, range = range)


@app.route("/search/name", methods = ['POST'])
@login_required
def post_search():
    """handles name search route"""
    name_form = SearchByNameForm()

    if name_form.validate_on_submit():
        name = name_form.name.data
        return redirect(f"/search/name/{name}")


@app.route("/search/ingredient", methods = ['POST'])
@login_required
def ingredient_search():
    """handles ingredient search route"""

    ingredient_form = SearchByIngredientForm()

    if ingredient_form.validate_on_submit():
        ingredient = ingredient_form.ingredient.data
        return redirect(f"/search/ingredient/{ingredient}")

@app.route("/drink/<drink_id>", methods = ["GET"])
@login_required
def drink_details(drink_id):
    """displays drink info"""
    cocktail = CocktailDetails.get_drink_by_id(drink_id)
    return render_template("display_cocktail.html", cocktail=cocktail)
    
@app.route("/drink/<drink_id>/save", methods=["POST"])
@login_required
def save_drink(drink_id):
    cocktail_from_api = CocktailDetails.get_drink_by_id(drink_id)
    my_cocktail = Cocktail(id = cocktail_from_api.drink_id, name=cocktail_from_api.name, drink_img_url=cocktail_from_api.img)
    db.session.add(my_cocktail)
    current_user.saved_cocktails.append(my_cocktail)
    db.session.commit()
    flash("Saved!")
    return redirect (f"/user/{current_user.id}")
    