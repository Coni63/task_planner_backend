from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Status
from django.urls import reverse
from django.contrib.auth.models import Permission
from core.models.custom_user import CustomUser


class StatusAPITestCase(APITestCase):
    def setUp(self):
        """Setup test data, including users and status"""
        self.user = CustomUser.objects.create_user(username="user", password="testpass")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass")

        self.set_permissions(self.user)

        self.status1 = Status.objects.create(status="status One")
        self.status2 = Status.objects.create(status="status Two", state="active")

        self.list_url = reverse("status-list")
        self.detail_url = reverse("status-detail", kwargs={"pk": self.status1.id})

        self.create_data = {
            "status": "New status",
            "state": "active",
        }
        self.update_data = {"status": "Updated status"}

    def set_permissions(self, user: CustomUser):
        view_status = Permission.objects.get(codename="view_status")
        change_status = Permission.objects.get(codename="change_status")
        delete_status = Permission.objects.get(codename="delete_status")
        add_status = Permission.objects.get(codename="add_status")
        user.user_permissions.add(view_status, change_status, delete_status, add_status)

    ## TEST CRUD OPERATIONS ##

    def test_get_status_list(self):
        """Ensure we can retrieve a list of status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_status_detail(self):
        """Ensure we can retrieve a single status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], self.status1.status)
        self.assertEqual(response.data["state"], "blocked")

    def test_create_status(self):
        """Ensure we can create a status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 3)

    def test_update_status(self):
        """Ensure we can update a status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.status, "Updated status")

    def test_delete_status(self):
        """Ensure we can delete a status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Status.objects.count(), 1)

    ## TEST PERMISSIONS ##

    def test_permission_list_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_list_not_allowed(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_create_anonymous(self):
        response = self.client.post(self.list_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_create_not_allowed(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.list_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_delete_anonymous(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_delete_not_allowed(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_update_anonymous(self):
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_update_not_allowed(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_read_anonymous(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_read_not_allowed(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
