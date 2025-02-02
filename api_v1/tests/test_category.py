from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Category
from django.urls import reverse
from django.contrib.auth.models import Permission
from core.models.custom_user import CustomUser


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        """Setup test data, including users and categories"""
        self.user = CustomUser.objects.create_user(username="user", password="testpass")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass")

        self.set_permissions(self.user)

        self.category1 = Category.objects.create(title="Category One")
        self.category2 = Category.objects.create(title="Category Two")

        self.list_url = reverse("category-list")
        self.detail_url = reverse("category-detail", kwargs={"pk": self.category1.id})

        self.create_data = {"title": "New Category", "junior_factor": 1.5, "senior_factor": 1.0}
        self.update_data = {"title": "Updated Category"}

    def set_permissions(self, user: CustomUser):
        view_category = Permission.objects.get(codename="view_category")
        change_category = Permission.objects.get(codename="change_category")
        delete_category = Permission.objects.get(codename="delete_category")
        add_category = Permission.objects.get(codename="add_category")
        user.user_permissions.add(view_category, change_category, delete_category, add_category)

    ## TEST CRUD OPERATIONS ##

    def test_get_category_list(self):
        """Ensure we can retrieve a list of categories"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_category_detail(self):
        """Ensure we can retrieve a single category"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.category1.title)
        self.assertEqual(response.data["junior_factor"], 2.0)

    def test_create_category(self):
        """Ensure we can create a category"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)

    def test_update_category(self):
        """Ensure we can update a category"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.title, "Updated Category")

    def test_delete_category(self):
        """Ensure we can delete a category"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)

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
