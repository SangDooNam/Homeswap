from django.test import TestCase
from django.core.files import File
from django.core.exceptions import ValidationError
from django.apps import apps
from pathlib import Path
from django.db import models as db

from datetime import datetime, timedelta
import datetime as dt
# Create your tests here.


BASE_DIR = Path(__file__).resolve().parent

class Test(TestCase):
    
    def setUp(self):
        self.appuser = apps.get_model('accounts', 'AppUser')
        profile_photo = open(BASE_DIR / "default.jpg", 'rb')
        self.appuser_params = {
            'username': 'unique_user',
            'email': 'user@email.com',
            'profile_photo': File(profile_photo, name='default.jpg'),
            'phone_number': '+4917633344234',
            'street': 'Beispielstraße',
            'location': 'Berlin',
            'max_capacity': 2,
            'postal_code': '12345',
        }
        
        self.blogpost = self.get_model('BlogPost')
        today = datetime.now()
        
        start_date = today + timedelta(days=7)
        
        self.blogpost_params = {
            'title' : 'test title',
            'user' : self.appuser.objects.create(**self.appuser_params),
            'location' : 'Berlin',
            'max_capacity': 3,
            'to_city': 'Seoul',
            'start_date': start_date,
            'end_date' : start_date + timedelta(days=7),
            'num_travelers' : 4,
            'description': 'test description',
        }
    
    def get_model(self, model_name=None):
        if not model_name:
            model_name = self.model_name
        try:
            model = apps.get_model('blog', model_name)
        except LookupError:
            model = None
        return model
    
    def test_model_names(self):
        self.assertIsNotNone(self.blogpost)
    
    
    def test_required_fields(self):
        params = self.appuser_params.copy()
        params['username'] = 'unique_user_required_fields'
        params['email'] = 'unique@email.com'
        params['phone_number'] = '+4917623473834'
        
        user = self.appuser.objects.create(**params)
        blogpost_params = self.blogpost_params.copy()
        blogpost_params['user'] = user
        blogpost_params['title'] = None
        blogpost_params['location'] = None
        blogpost_params['max_capacity'] = None
        blogpost_params['to_city'] = None
        blogpost_params['end_date'] = None
        blogpost_params['description'] = None

        blogpost = self.blogpost(**blogpost_params)
        with self.assertRaises(ValidationError) as cm:
            blogpost.full_clean()

        e = cm.exception
        fields = e.message_dict.keys()
        self.assertIn('title', fields)
        self.assertIn('location', fields)
        self.assertIn('max_capacity', fields)
        self.assertIn('to_city', fields)
        self.assertIn('end_date', fields)
        self.assertIn('description', fields)
    
    def test_max_length_validation(self):
        
        params = self.appuser_params.copy()
        params['username'] = 'unique_user_length_validation'
        params['email'] = 'length@email.com'
        params['phone_number'] = '+4917623343834'
        
        user = self.appuser.objects.create(**params)
        blogpost_params = self.blogpost_params.copy()
        blogpost_params['user'] = user
        blogpost_params['location'] = 'a' * 101
        blogpost_params['to_city'] = 'b' * 101
        blogpost = self.blogpost(**blogpost_params)
        with self.assertRaises(ValidationError) as cm:
            blogpost.full_clean()
        
        e = cm.exception
        fields = e.message_dict.keys()
        self.assertIn('location', fields)
        self.assertIn('to_city', fields)
    
    def test_start_date(self):
        
        params = self.appuser_params.copy()
        params['username'] = 'unique_user_start_date'
        params['email'] = 'start@email.com'
        params['phone_number'] = '+4917623773834'
        
        today = dt.date.today()
        older_than_today = today - timedelta(days=7)
        
        user = self.appuser.objects.create(**params)
        blogpost_params = self.blogpost_params.copy()
        blogpost_params['user'] = user
        blogpost_params['start_date'] = older_than_today
        
        blogpost = self.blogpost(**blogpost_params)
        with self.assertRaises(ValidationError) as cm:
            blogpost.full_clean()
        
        e = cm.exception
        fields = e.message_dict.keys()
        self.assertIn('start_date', fields)
        
    def test_end_date(self):
        
        params = self.appuser_params.copy()
        params['username'] = 'unique_user_end_date'
        params['email'] = 'end@email.com'
        params['phone_number'] = '+4912323773834'
        
        today = dt.date.today()
        older_than_today = today - timedelta(days=7)
        
        user = self.appuser.objects.create(**params)
        blogpost_params = self.blogpost_params.copy()
        blogpost_params['user'] = user
        blogpost_params['end_date'] = older_than_today
        
        blogpost = self.blogpost(**blogpost_params)
        with self.assertRaises(ValidationError) as cm:
            blogpost.full_clean()
        
        e = cm.exception
        fields = e.message_dict.keys()
        self.assertIn('end_date', fields)
        
    def test_num_travelers(self):
        params = self.appuser_params.copy()
        params['username'] = 'unique_user_num_travelers'
        params['email'] = 'travelers@email.com'
        params['phone_number'] = '+4917623712834'
        user = self.appuser.objects.create(**params)
        blogpost_params = self.blogpost_params.copy()
        blogpost_params['user'] = user
        blogpost_params['num_travelers'] = 0
        
        blogpost = self.blogpost(**blogpost_params)
        with self.assertRaises(ValidationError) as cm:
            blogpost.full_clean()
        
        e = cm.exception
        fields = e.message_dict.keys()
        self.assertIn('num_travelers', fields)
        
    def test_foreign_keys(self):
    
        field = self.blogpost._meta.get_field("user")

        self.assertTrue(isinstance(field, db.ForeignKey))