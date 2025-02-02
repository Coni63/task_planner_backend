from rest_framework import status
from rest_framework.test import APITestCase
from core.models import UserAssignment
from django.urls import reverse
from django.contrib.auth.models import Permission
from core.models.category import Category
from core.models.custom_user import CustomUser

class UserAssignmentAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user", password="testpass")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass")

        self.set_permissions(self.user)

        self.category1 = Category.objects.create(title="Category One")
        self.category2 = Category.objects.create(title="Category Two")

        self.assignment1 = UserAssignment.objects.create(user=self.user, category=self.category1, level="Senior")
        self.assignment2 = UserAssignment.objects.create(user=self.user2, category=self.category1, level="Junior")

        self.list_url = reverse("user-assignement-list")
        self.detail_url = reverse("user-assignement-detail", kwargs={"pk": self.assignment1.id})

        self.create_data = {"user": str(self.user.id), "level": "Medior", "category": str(self.category2.id)}
        self.create_data_duplicated = {"user": str(self.user.id), "level": "Medior", "category": str(self.category1.id)}
        self.update_data = {"level": "Senior"}

    def set_permissions(self, user: CustomUser):
        view_perm = Permission.objects.get(codename="view_userassignment")
        change_perm = Permission.objects.get(codename="change_userassignment")
        delete_perm = Permission.objects.get(codename="delete_userassignment")
        add_perm = Permission.objects.get(codename="add_userassignment")
        user.user_permissions.add(view_perm, change_perm, delete_perm, add_perm)

    def test_get_user_assignment_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_assignment_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["level"], self.assignment1.level)

    def test_create_user_assignment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserAssignment.objects.count(), 3)

    def test_create_duplicated_user_assignment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.create_data_duplicated)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserAssignment.objects.count(), 2)

    def test_update_user_assignment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assignment1.refresh_from_db()
        self.assertEqual(self.assignment1.level, "Senior")

    def test_delete_user_assignment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserAssignment.objects.count(), 1)

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
