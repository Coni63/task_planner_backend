from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Project
from django.urls import reverse
from django.contrib.auth.models import Permission

from core.models.custom_user import CustomUser

class ProjectAPITestCase(APITestCase):

    def setUp(self):
        """Setup test data, including users and projects"""
        self.user = CustomUser.objects.create_user(username="user", password="testpass")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass")

        self.set_permissions(self.user)

        self.project1 = Project.objects.create(
            name="Project One",
            description="Test project",
            trigram="P01",
            order=1
        )
        
        self.project2 = Project.objects.create(
            name="Project Two",
            description="Another test project",
            trigram="P02",
            order=2
        )

        self.list_url = reverse("project-list")  # Name from your URL patterns
        self.detail_url = reverse("project-detail", kwargs={"pk": self.project1.id})

        self.create_data = {
            "name": "New Project",
            "description": "A new project",
            "trigram": "NP1",
            "order": 3
        }
        self.update_data = {"name": "Updated Project"}

    def set_permissions(self, user: CustomUser):
        view_project = Permission.objects.get(codename="view_project")
        change_project = Permission.objects.get(codename="change_project")
        delete_project = Permission.objects.get(codename="delete_project")
        add_project = Permission.objects.get(codename="add_project")
        user.user_permissions.add(view_project)
        user.user_permissions.add(change_project)
        user.user_permissions.add(delete_project)
        user.user_permissions.add(add_project)


    ## TEST CRUD OPERATIONS ##

    def test_get_project_list(self):
        """Ensure we can retrieve a list of projects"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_project_detail(self):
        """Ensure we can retrieve a single project"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.project1.name)

    def test_create_project(self):
        """Ensure we can create a project"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 3)

    def test_update_project(self):
        """Ensure we can update a project"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, "Updated Project")

    def test_delete_project(self):
        """Ensure we can delete a project"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 1)

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

