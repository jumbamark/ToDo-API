from django.test import TestCase
from rest_framework.test import APITestCase
from authentication.models import User

# Create your tests here.
class TestModel(APITestCase):
    def test_creates_user(self):
        user = User.objects.create_user("gathoni", "gathoni@outlook.com", "Nonnie")
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, "gathoni@outlook.com")

    def test_creates_super_user(self):
        user = User.objects.create_superuser("gathoni", "gathoni@outlook.com", "Nonnie")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, "gathoni@outlook.com")

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="", email="gathoni@outlook.com", password="Nonnie")
        # self.assertRaisesMessage(ValueError, "The given username must be set")
    
    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given username must be set"):
            User.objects.create_user(username="", email="gathoni@outlook.com", password="Nonnie")

    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="gathoni", email="", password="Nonnie")

    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            User.objects.create_user(username="gathoni", email="", password="Nonnie")

    def test_cant_create_superuser_with_no_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(username="gathoni", email="", password="Nonnie", is_staff=False)

    def test_cant_create_super_user_with_no_is_super_user_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(username="gathoni", email="", password="Nonnie", is_superuser=False)
