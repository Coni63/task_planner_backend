from rest_framework import status
from rest_framework.test import APITestCase
from core.models import WorkflowTransition
from django.urls import reverse
from django.contrib.auth.models import Permission
from core.models.custom_user import CustomUser
from core.models.status import Status


class WorkflowTransitionAPITestCase(APITestCase):
    def setUp(self):
        """Setup test data, including users and status"""
        self.user = CustomUser.objects.create_user(username="user", password="testpass")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass")

        self.set_permissions(self.user)

        self.project = Status.objects.create(status="status One")
        self.status2 = Status.objects.create(status="status Two")
        self.status3 = Status.objects.create(status="status Three")

        self.workflow1 = WorkflowTransition.objects.create(name="T1", from_status=self.status1, to_status=self.status2)
        self.workflow2 = WorkflowTransition.objects.create(name="T2", from_status=self.status2, to_status=self.status3)

        self.list_url = reverse("workflow-list")
        self.detail_url = reverse("workflow-detail", kwargs={"pk": self.workflow1.id})

        self.create_data = {"name": "T3", "from_status": str(self.status1.id), "to_status": str(self.status3.id)}
        self.update_data = {"name": "Updated workflow"}

    def set_permissions(self, user: CustomUser):
        view_workflow = Permission.objects.get(codename="view_workflowtransition")
        change_workflow = Permission.objects.get(codename="change_workflowtransition")
        delete_workflow = Permission.objects.get(codename="delete_workflowtransition")
        add_workflow = Permission.objects.get(codename="add_workflowtransition")
        user.user_permissions.add(view_workflow, change_workflow, delete_workflow, add_workflow)

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
        self.assertEqual(response.data["name"], self.workflow1.name)

    def test_create_status(self):
        """Ensure we can create a status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkflowTransition.objects.count(), 3)

    def test_update_status(self):
        """Ensure we can update a status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workflow1.refresh_from_db()
        self.assertEqual(self.workflow1.name, "Updated workflow")

    def test_delete_status(self):
        """Ensure we can delete a status"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkflowTransition.objects.count(), 1)

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
