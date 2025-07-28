from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_user_email(self):
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')