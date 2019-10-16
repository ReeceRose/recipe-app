from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@reecerose.com',
            password='Testingpassword123!'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='test@reecerose.com',
            password='Testingpassword123!',
            name='Test User'
        )

    def test_users_listed(self):
        """Test that users are listed on user page. Returns successful"""
        # Arrange
        url = reverse('admin:core_user_changelist')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works. Returns successful"""
        # Arrange
        # returns (/admin/core/user/ID/)
        url = reverse('admin:core_user_change', args=[self.user.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works. Returns successful"""
        # Arrange
        url = reverse('admin:core_user_add')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
