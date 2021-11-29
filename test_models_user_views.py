
from unittest import TestCase
from models import db, User, Cocktail, Saved, UserCocktail, UserCocktailIngredient




from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://@localhost:5433/test_cocktail"

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserModelTestCase(TestCase):
    """Tests user model"""

    def setUp(self):
        """create test client, add sample data."""
        
        Saved.query.delete()
        UserCocktail.query.delete()
        UserCocktailIngredient.query.delete()
        Cocktail.query.delete()
        User.query.delete()
        
        

        self.client = app.test_client

    def test_user_model(self):
        """does user model work"""

        u = User(
            id = "1",
            username = "testname",
            password = "HASHED_PASSWORD",
            email = "testemail@test.com", 
            dob = "01/01/2000"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.saved_cocktails), 0)
        self.assertEqual(len(u.user_cocktails), 0)

    def test_home_page(self):
        with app.test_client() as client:

            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to Cocktail Hour", html)


    def test_login(self):
        with app.test_client() as client:

            resp = client.post('/login', data = {'username': 'testname', 'password': 'testuser'}, follow_redirects = True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            
    def test_invalid_password(self):
        with app.test_client() as client:

            resp = client.post(
                '/login', data={'username': 'testname', 'password': 'nottestuser'}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid username or password", html)    

    def test_signup(self):
        with app.test_client() as client:

            resp = client.post('/signup', data = {'username': 'testname', 'email': 'testemail@test.com', 'password': 'newpassword', 'dob': '01/02/1999'}, follow_redirects = True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("testname", html)
    
    def test_delete_user(self):
        with app.test_client() as client:

            resp = client.post(f"/user/1/delete", follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('testname', html)
    
    def test_logout(self):
        with app.test_client() as client:

            resp = client.post('/logout/1', follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('testname', html)


    