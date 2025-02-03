from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import CustomUser

class UserAPITestCase(APITestCase):
    
    def setUp(self):
        """Setup test data, including users"""
        self.user1 = CustomUser.objects.create_user(username="user1", password="testpass")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass")
        
        self.list_url = reverse("user-list")  # Ensure your URL patterns match
        self.detail_url = reverse("user-detail", kwargs={"pk": self.user1.id})
        
        self.update_data = {"name": "updated_user"}  # the username is binded to username for the UI

    ## TEST CRUD OPERATIONS ##

    def test_get_user_list(self):
        """Ensure we can retrieve a list of users"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_user_detail(self):
        """Ensure we can retrieve a single user"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.user1.username)
    
    def test_update_own_user(self):
        """Ensure a user can update their own profile"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "updated_user")
    
    def test_update_other_user_forbidden(self):
        """Ensure a user cannot update another user's profile"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_own_user(self):
        """Ensure a user can delete their own account"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=self.user1.id).exists())
    
    def test_delete_other_user_forbidden(self):
        """Ensure a user cannot delete another user's account"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    ## TEST PERMISSIONS ##
    
    def test_permission_list_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_permission_read_other(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_permission_update_anonymous(self):
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_permission_update_other(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_permission_delete_anonymous(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)