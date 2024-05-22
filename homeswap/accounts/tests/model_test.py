from django.test import TestCase
from django.core.files import File
from django.core.exceptions import ValidationError
from django.apps import apps
from django.db import models as db
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Test(TestCase):

    def setUp(self) -> None:
        """Set up."""
        super().setUp()

        self.appuser = self.get_model('AppUser')
        self.homephoto = self.get_model('HomePhoto')

        profile_photo = open(BASE_DIR / "default.jpg", 'rb')
        home_photo = open(BASE_DIR / 'test_home_photo_1.jpg', 'rb')

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

        self.homephoto_params = {
            'user': self.appuser.objects.create(**self.appuser_params),
            'image': File(home_photo, name='test_home_photo_1.jpg'),
            'photo_type': 'bed room',
        }

    def get_model(self, model_name=None):
        if not model_name:
            model_name = self.model_name
        try:
            model = apps.get_model('accounts', model_name)
        except LookupError:
            model = None
        return model

    def test_model_names(self):
        self.assertIsNotNone(self.appuser)
        self.assertIsNotNone(self.homephoto)

    def test_required_fields(self):

        with self.assertRaises(ValidationError) as cm:
            self.homephoto.objects.create()
        e = cm.exception
        fields = [error[0] for error in e]
        self.assertEqual(len(fields), 2)
        self.assertIn('user', fields)
        self.assertIn('photo_type', fields)

    def test_phone_number(self):
        params = self.appuser_params.copy()
        params['username'] = 'unique_phone_number'
        params['phone_number'] = '+123'
        with self.assertRaises(ValidationError) as cm:
            user = self.appuser(**params)
            user.clean()
        e = cm.exception
        print('ERROR: ',e)
        fields = [error[0] for error in e]
        self.assertIn('phone_number', fields)
        
        
    def test_postal_code(self):
        params = self.appuser_params.copy()
        params['postal_code'] = 'A' * 14
        params['username'] = 'unique_user_for_test'
        with self.assertRaises(ValidationError) as cm:
            user = self.appuser(**params)
            user.clean()
        e = cm.exception
        fields = [error[0] for error in e]
        self.assertIn('postal_code', fields)
        
        
        params = self.appuser_params.copy()
        params['postal_code'] = 'ABCDE'
        params['username'] = 'unique_user_postal_code'  
        with self.assertRaises(ValidationError) as cm:
            user = self.appuser(**params)
            user.clean()
        e = cm.exception
        fields = [error[0] for error in e]
        self.assertIn('postal_code', fields)

    def test_string_lengths(self):
        params = self.appuser_params.copy()
        params['street'] = 'a' * 41  
        params['username'] = 'unique_user_string_lengths' 

        with self.assertRaises(ValidationError) as cm:
            user = self.appuser(**params)
            user.clean()
        e = cm.exception
        fields = e.error_dict.keys()
        self.assertIn('street', fields)
        
        params = self.appuser_params.copy()
        params['location'] = 'a' * 41 
        params['username'] = 'nice_user_name'
        
        with self.assertRaises(ValidationError) as cm:
            user = self.appuser(**params)
            user.clean()
        e = cm.exception
        fields = e.error_dict.keys()
        self.assertIn('location', fields)

    def test_foreign_keys(self):
        field = self.homephoto._meta.get_field("user")
        self.assertTrue(isinstance(field, db.ForeignKey))
