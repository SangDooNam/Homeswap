from django.test import TestCase
from django.core.files import File
from django.core.exceptions import ValidationError
from django.apps import apps
from django.db import models as db
from pathlib import Path
from django.utils import timezone
from datetime import datetime, timedelta
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
        pass