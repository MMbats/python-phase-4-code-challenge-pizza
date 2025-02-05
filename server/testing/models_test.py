import unittest
import pytest
from faker import Faker
from server.app import app, db
from server.models import Restaurant, Pizza, RestaurantPizza

class TestRestaurantPizza(unittest.TestCase):
    '''Class RestaurantPizza in models.py'''

    def setUp(self):
        """Set up test database"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_price_between_1_and_30(self):
        '''requires price between 1 and 30.'''
        with app.app_context():
            pizza = Pizza(
                name=Faker().name(), ingredients="Dough, Sauce, Cheese")
            restaurant = Restaurant(name=Faker().name(), address='Main St')
            db.session.add(pizza)
            db.session.add(restaurant)
            db.session.commit()

            restaurant_pizza = RestaurantPizza(
                price=15,
                pizza_id=pizza.id,
                restaurant_id=restaurant.id
            )
            db.session.add(restaurant_pizza)
            db.session.commit()

            self.assertEqual(restaurant_pizza.price, 15)

    def test_price_too_low(self):
        '''requires price between 1 and 30 and fails when price is 0.'''
        with app.app_context():
            with pytest.raises(ValueError):
                pizza = Pizza(
                    name=Faker().name(), ingredients="Dough, Sauce, Cheese")
                restaurant = Restaurant(name=Faker().name(), address='Main St')
                db.session.add(pizza)
                db.session.add(restaurant)
                db.session.commit()

                restaurant_pizza = RestaurantPizza(
                    price=0,  # Invalid price
                    pizza_id=pizza.id,
                    restaurant_id=restaurant.id
                )
                db.session.add(restaurant_pizza)
                db.session.commit()

    def test_price_too_high(self):
        '''requires price between 1 and 30 and fails when price is 31.'''
        with app.app_context():
            with pytest.raises(ValueError):
                pizza = Pizza(
                    name=Faker().name(), ingredients="Dough, Sauce, Cheese")
                restaurant = Restaurant(name=Faker().name(), address='Main St')
                db.session.add(pizza)
                db.session.add(restaurant)
                db.session.commit()

                restaurant_pizza = RestaurantPizza(
                    price=31,  # Invalid price
                    pizza_id=pizza.id,
                    restaurant_id=restaurant.id
                )
                db.session.add(restaurant_pizza)
                db.session.commit()