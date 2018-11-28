import os
from flask import Flask, request
import unittest
from urllib.request import urlopen
from flask_testing import TestCase
from flask_login import current_user
from app import app, db
from app import User, Items

# To run tests...
# Make sure the server is running 'sudo service postgresql start'
# Enter 'python3 tests.py'

class BaseTestCase(TestCase):
    
    def create_app(self):
        app.debug = True
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app
    
    def setUp(self):
        db.create_all()
        db.session.add(User(username='TestUser', email='testuser@domain.com', password='Resutset'))
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class ViewsTest(BaseTestCase):
    
    def setUp(self):
        
        self.client = app.test_client()
        self.client.testing = True
    
    def tearDown(self):
        
        pass
    
    def create_app(self):

        app = Flask('__name__')
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0
        return app
    
class TestViewsAndFunctions(BaseTestCase):
    
    def test_index_page(self):
        
        response = self.client.get('/')

        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed('index.html')
        self.assertTrue(b"Welcome to Next Man's Treasure" in response.data)
    
    def test_user_page(self):
        
        response = self.client.get('/user')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed('user.html')
        self.assertIn(b"Log in to your account", response.data)
    
    def test_user_page_login_correct_credentials(self):
            
        response = self.client.post('/login', data=dict(username='TestUser',
                                              password='Resutset'),
                                              follow_redirects=True)
        
        """ Test to ensure recognised users can log in with the correct credentials """
        self.assertIn(b"Welcome to your account, TestUser!", response.data)
    
    def test_user_page_register_valid_credentials(self):
        
        response = self.client.post('/add_user', data=dict(username='Test2',
                                                 email='testing2@test.com',
                                                 password='Test2'),
                                                 follow_redirects=True)
        
        """ Test to ensure users can register with valid credentials """
        self.assertIn(b"Welcome to your account, Test2!", response.data)
    
    def test_logout(self):
            
        response = self.client.get('/logout', follow_redirects=True)
        
        """ Tests logout function follows correct redirect path """
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Next Man's Treasure", response.data)
    
    def test_account_page(self):
        
        response = self.client.get('/account')
        
        """ Tests pages response status code is 401 when user is unauthorised """
        self.assertEqual(response.status_code, 401)

    def test_sell_page(self):
            
        response = self.client.get('/sell')
        
        """ Tests pages response status code is 401 when user is unauthorised """
        self.assertEqual(response.status_code, 401)
        
    def test_listed_page(self):
            
        response = self.client.get('/listed')
        
        """ Tests pages response status code is 401 when user is unauthorised """
        self.assertEqual(response.status_code, 401)

    def test_browse_brand_page(self):
        
        response = self.client.get('/browse_brand')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed('browse_brand.html')
        self.assertTrue(b"Browse by brand" in response.data)

    def test_browse_gender_page(self):
        
        response = self.client.get('/browse_gender')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed('browse_gender.html')
        self.assertTrue(b"Browse by gender" in response.data)

    def test_view_listing_page(self):
        
        id = 1
        response = self.client.get('/view_listing/{0}'.format(id))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed('view_listing.html')

    def test_edit_listing_page(self):
        
        id = 1
        response = self.client.get('/edit_listing/{0}'.format(id))
        
        """ Tests non-authorised users can't access page by retrieving response status code """
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()