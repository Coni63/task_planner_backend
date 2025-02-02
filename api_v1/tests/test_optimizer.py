from datetime import datetime, timezone
import uuid
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from core.models.custom_user import CustomUser
from core.models.project import Project
from unittest.mock import patch
from django_q.models import Task as QTask


class OptimizerAPITestCase(APITestCase):
    def setUp(self):
        """Setup test data, including users and status"""
        self.user = CustomUser.objects.create_user(username="user", password="testpass")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass")

        self.set_permissions(self.user)

        self.project = Project.objects.create(name="Project One", description="Test project", trigram="P01", order=1)
        self.mock_task = QTask.objects.create(
            id="f899cf40-d242-43be-a259-9b19e25a9cdb",
            name="MyTask",
            success=True,
            started=datetime.now(tz=timezone.utc),
            stopped=datetime.now(tz=timezone.utc),
        )

        self.submit_url = reverse("optimizer-submit")
        self.status_url = reverse("optimizer-status", kwargs={"pk": self.mock_task.id})

        self.create_data = {
            "project_id": str(self.project.id),
        }

    def set_permissions(self, user: CustomUser):
        view_queue = Permission.objects.get(codename="view_ormq")
        add_queue = Permission.objects.get(codename="add_ormq")
        user.user_permissions.add(view_queue, add_queue)

    ## TEST CRUD OPERATIONS ##

    @patch("api_v1.views.optimizer_view.async_task")
    def test_create_status(self, mock_async_task):
        """Ensure we can create a status"""
        mock_async_task.return_value = "f899cf40-d242-43be-a259-9b19e25a9cdb"

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.submit_url, self.create_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["task_id"], "f899cf40-d242-43be-a259-9b19e25a9cdb")

        mock_async_task.assert_called_once_with("optimization.services.optimize", self.create_data)

    @patch("api_v1.views.optimizer_view.fetch")
    def test_get_status(self, mock_fetch):
        """Ensure we can fetch a task's status"""
        mock_fetch.return_value = self.mock_task

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.status_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

        mock_fetch.assert_called_once_with(uuid.UUID(self.mock_task.id))

    ## TEST PERMISSIONS ##

    def test_permission_create_anonymous(self):
        response = self.client.post(self.submit_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_create_not_allowed(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.submit_url, self.create_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_read_anonymous(self):
        response = self.client.get(self.status_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_read_not_allowed(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.status_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
