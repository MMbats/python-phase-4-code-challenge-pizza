import unittest
from server.app import app, db
from faker import Faker

class TestApp(unittest.TestCase):
    '''Flask application in app.py'''

    def setUp(self):
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()