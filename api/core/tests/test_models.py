from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@reecerose.com', password='Testingpassword123!'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email. Return successful"""
        # Arrange
        email = 'test@reecerose.com'
        password = 'Testingpassword123!'
        # Act
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # Assert
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized. Returns successful"""
        # Arrange
        email = 'test@REECEROSE.COM'
        # Act
        user = get_user_model().objects.create_user(
            email=email,
            password='Testingpassword123!'
        )
        # Assert
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email. Raises error"""
        # Assert
        with self.assertRaises(ValueError):
            # Arrange, Act
            get_user_model().objects.create_user(None, 'Testingpassword123!')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        # Arrange, Act
        user = get_user_model().objects.create_superuser(
            email='test@reecerose.com',
            password='Testingpassword123!'
        )
        # Assert
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_string(self):
        """Test the tag string"""
        # Arrange
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        # Assert
        self.assertEqual(str(tag), tag.name)
