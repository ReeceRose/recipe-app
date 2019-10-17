from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagApiTests(TestCase):
    """Test the publicaly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that logic is required for retrieving tags"""
        # Arrange/Act
        response = self.client.get(TAGS_URL)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the private tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@reecerose.com',
            'Testpassword123!'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        # Arrange
        Tag.objects.create(user=self.user, name='Dessert')
        Tag.objects.create(user=self.user, name='Vegan')
        # Act
        response = self.client.get(TAGS_URL)
        # Assert
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limtied_to_user(self):
        """Test that tags returned are for the authenticated user"""
        # Arrange
        user2 = get_user_model().objects.create_user(
            'user@reecerose.com',
            'Testpassword123!'
        )
        Tag.objects.create(user=user2, name='Fruit')
        tag = Tag.objects.create(user=self.user, name='Dessert')
        # Act
        response = self.client.get(TAGS_URL)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        # Arrange
        payload = {'name': 'Test Tag'}
        # Act
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        # Assert
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        # Arrange
        payload = {'name': ''}
        # Act
        response = self.client.post(TAGS_URL, payload)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
