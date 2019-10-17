from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
LOGIN_URL = reverse('user:login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_sucess(self):
        """Test creating user with valid payload. Returns success"""
        # Arrange
        payload = {
            'email': 'test@reecerose.com',
            'password': 'Testingpassword123!',
            'name': 'Test Name'
        }
        # Act
        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**response.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating a user that already exists. Returns error"""
        # Arrange
        payload = {
            'email': 'test@reecerose.com',
            'password': 'Testingpassword123!',
            'name': 'Test Name'
        }
        create_user(**payload)
        # Act
        response = self.client.post(CREATE_USER_URL, payload)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be < 5 characters. Returns error"""
        # Arrange
        payload = {
            'email': 'test@reecerose.com',
            'password': '1234',
        }
        # Act
        response = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for a user"""
        # Arrange
        payload = {
            'email': 'test@reecerose.com',
            'password': 'Testingpassword123!',
        }
        create_user(**payload)
        # Act
        response = self.client.post(LOGIN_URL, payload)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created when invalid credentials passed"""
        # Arrange
        create_user(email="test@reecerose.com", password="Testingpassword123!")
        payload = {
            'email': 'test@reecerose.com',
            'password': 'Testingpassword1!',
        }
        # Act
        response = self.client.post(LOGIN_URL, payload)
        # Assert
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that a token is not created when use does not exist"""
        payload = {
            'email': 'test@reecerose.com',
            'password': 'Testingpassword1!',
        }
        # Act
        response = self.client.post(LOGIN_URL, payload)
        # Assert
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        # Arrange/Act
        response = self.client.post(LOGIN_URL, {
            'email': 'test@reecerose.com',
            'password': ''
        })
        # Assert
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
