import app
import unittest
from polifinder_app.models import db, User
from polifinder_app.extensions import db, app, bcrypt

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

class AuthTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    
    def test_signup(self):
        post_data = {
            'username': 'Helloworld',
            'password': 'password'
        }
        self.app.post('/signup', data=post_data)
        response = self.app.get('/profile/Helloworld')
        response_text = response.get_data(as_text=True)
        self.assertIsNotNone('Helloworld', response_text)

    def test_signup_existing_user(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('That username already exists.', response_text)

    def test_login_nonexistent_user(self):
        post_data = {
            'username': 'Hillary5evr',
            'password': 'Hilldawg'
        }
        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('Invalid credentials.', response_text)
    
    def test_login_correct_password(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        response = self.app.get('/login', data=post_data)
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertNotIn('login', response_text)

    def test_login_incorrect_password(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'ewneocon'
        }
        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('Invalid credentials.', response_text)

    def test_logout(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/login', data=post_data)
        self.app.get('/logout')
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('login', response_text)