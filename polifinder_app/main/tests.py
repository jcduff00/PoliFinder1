import unittest
import app
from polifinder_app.extensions import app, db, bcrypt
from polifinder_app.models import Politician, District, User

"""
Run these tests with the command:
python3 -m unittest aquaritrack.main.tests
"""

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_politicians():
    a1 = District(name='CA30', state='California', region='West Coast')
    db.session.add(a1)

    b1 = Politician(
        name = 'Marianne Williamson', 
        office = 'Congresswoman', 
        party = 'DEMOCRATIC',
        photo_url = 'test',
        district = a1,
        )
    db.session.add(b1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

class MainTests(unittest.TestCase):
 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_in(self):
        create_politicians()
        create_user()
        login(self.app, 'me1', 'password')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Marianne Williamson', response_text)
        self.assertIn('New District', response_text)
        self.assertIn('New Politician', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)