from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


from .permissions import CustomJWTAuthentication, IsAdminUser
from .models import Category, Project, Status, Task, CustomUser, UserAssignment
from .serializers import (
    CategorySerializer,
    ProjectSerializer,
    StatusSerializer,
    TaskSerializer,
    TaskSimpleSerializer,
    UserAssignmentSerializer,
    UserAssignmentSimpleSerializer,
    UserSerializer,
)


class UserList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        """
        Retrieve all users.
        """
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request, user_id: str) -> Response:
        """
        Retrieve a single user by ID.
        """
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User not found")

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        """
        Retrieve all categories.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAssignmentList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        """
        Retrieve all user assignments or for a single user (by id with query param 'user')
        """
        user_id = request.query_params.get("user")
        if user_id:
            user_assignments = UserAssignment.objects.filter(user=user_id)
            if not user_assignments.exists():
                return Response([], status=status.HTTP_204_NO_CONTENT)
        else:
            user_assignments = UserAssignment.objects.all()

        serializer = UserAssignmentSerializer(user_assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        Create a new user assignment.
        """
        serializer = UserAssignmentSimpleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAssignmentDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request, assignment_id: str) -> Response:
        """
        Get a single user assignment by id.
        """
        try:
            user_assignments = UserAssignment.objects.get(pk=assignment_id)
        except UserAssignment.DoesNotExist:
            raise NotFound(detail="UserAssignment not found")

        serializer = UserAssignmentSerializer(user_assignments)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, assignment_id: str) -> Response:
        """
        Delete a user assignment by id.
        """
        try:
            user_assignment = UserAssignment.objects.get(pk=assignment_id)
            user_assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserAssignment.DoesNotExist:
            raise NotFound(detail="UserAssignment not found")

    def put(self, request: Request, assignment_id: str) -> Response:
        """
        Update a user assignment by id.
        """
        try:
            user_assignment = UserAssignment.objects.get(pk=assignment_id)
        except UserAssignment.DoesNotExist:
            raise NotFound(detail="UserAssignment not found")

        serializer = UserAssignmentSerializer(user_assignment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        """	
        Retrieve all projects.
        """
        projects = Project.objects.all()  # noqa: F821
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new project.
        """
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request: Request, project_id: str) -> Response:
        """
        Retrieve a single project by ID.
        """
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, project_id: str):
        """
        Delete a project by ID.
        """
        try:
            project = Project.objects.get(pk=project_id)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

    def put(self, request: Request, project_id: str):
        """
        Update a project by ID.
        """
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(project, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        """
        Retrieve all statuses.
        """
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)


class StatusDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request, status_id: str) -> Response:
        """
        Retrieve a single status by ID.
        """
        try:
            records = Status.objects.get(pk=status_id)
        except Status.DoesNotExist:
            raise NotFound(detail="Status not found")

        serializer = StatusSerializer(records)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        """
        Retrieve all tasks or for a single project (by id with query param 'project')
        """
        project_id = request.query_params.get("project")
        if project_id:
            tasks = Task.objects.filter(project=project_id)
            if not tasks.exists():
                return Response([], status=status.HTTP_204_NO_CONTENT)
        else:
            tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new task.
        """
        serializer = TaskSimpleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request, task_id: str) -> Response:
        """
        Retrieve a single task by ID.
        """
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found")

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, task_id: str):
        """
        Delete a task by ID.
        """
        try:
            task = Task.objects.get(pk=task_id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            raise NotFound(detail="Project not found")

    def put(self, request: Request, task_id: str):
        """
        Update a task by ID.
        """
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = TaskSimpleSerializer(task, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Myself(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Retrieve the current user.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MyMenu(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Retrieve the current user's menu.
        """
        if not request.user.is_active:
            return Response([], status=status.HTTP_204_NO_CONTENT)

        if request.user.is_admin or request.user.is_superuser:
            return Response([{
  "menu": [
    {
      "route": "dashboard",
      "name": "dashboard",
      "type": "link",
      "icon": "dashboard",
      "badge": {
        "color": "red-50",
        "value": "5"
      }
    },
    {
      "route": "design",
      "name": "design",
      "type": "sub",
      "icon": "color_lens",
      "label": {
        "color": "azure-50",
        "value": "New"
      },
      "children": [
        {
          "route": "colors",
          "name": "colors",
          "type": "link",
          "icon": "colorize"
        },
        {
          "route": "icons",
          "name": "icons",
          "type": "link",
          "icon": "flag"
        }
      ],
      "permissions": {
        "only": [
          "ADMIN",
          "MANAGER"
        ]
      }
    },
    {
      "route": "material",
      "name": "material",
      "type": "sub",
      "icon": "favorite",
      "children": [
        {
          "route": "",
          "name": "form-controls",
          "type": "sub",
          "children": [
            {
              "route": "autocomplete",
              "name": "autocomplete",
              "type": "link"
            },
            {
              "route": "checkbox",
              "name": "checkbox",
              "type": "link"
            },
            {
              "route": "datepicker",
              "name": "datepicker",
              "type": "link"
            },
            {
              "route": "form-field",
              "name": "form-field",
              "type": "link"
            },
            {
              "route": "input",
              "name": "input",
              "type": "link"
            },
            {
              "route": "radio",
              "name": "radio",
              "type": "link"
            },
            {
              "route": "select",
              "name": "select",
              "type": "link"
            },
            {
              "route": "slider",
              "name": "slider",
              "type": "link"
            },
            {
              "route": "slide-toggle",
              "name": "slide-toggle",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "navigation",
          "type": "sub",
          "children": [
            {
              "route": "menu",
              "name": "menu",
              "type": "link"
            },
            {
              "route": "sidenav",
              "name": "sidenav",
              "type": "link"
            },
            {
              "route": "toolbar",
              "name": "toolbar",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "layout",
          "type": "sub",
          "children": [
            {
              "route": "card",
              "name": "card",
              "type": "link"
            },
            {
              "route": "divider",
              "name": "divider",
              "type": "link"
            },
            {
              "route": "expansion",
              "name": "expansion",
              "type": "link"
            },
            {
              "route": "grid-list",
              "name": "grid-list",
              "type": "link"
            },
            {
              "route": "list",
              "name": "list",
              "type": "link"
            },
            {
              "route": "stepper",
              "name": "stepper",
              "type": "link"
            },
            {
              "route": "tab",
              "name": "tab",
              "type": "link"
            },
            {
              "route": "tree",
              "name": "tree",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "buttons-indicators",
          "type": "sub",
          "children": [
            {
              "route": "button",
              "name": "button",
              "type": "link"
            },
            {
              "route": "button-toggle",
              "name": "button-toggle",
              "type": "link"
            },
            {
              "route": "badge",
              "name": "badge",
              "type": "link"
            },
            {
              "route": "chips",
              "name": "chips",
              "type": "link"
            },
            {
              "route": "icon",
              "name": "icon",
              "type": "link"
            },
            {
              "route": "progress-spinner",
              "name": "progress-spinner",
              "type": "link"
            },
            {
              "route": "progress-bar",
              "name": "progress-bar",
              "type": "link"
            },
            {
              "route": "ripple",
              "name": "ripple",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "popups-modals",
          "type": "sub",
          "children": [
            {
              "route": "bottom-sheet",
              "name": "bottom-sheet",
              "type": "link"
            },
            {
              "route": "dialog",
              "name": "dialog",
              "type": "link"
            },
            {
              "route": "snack-bar",
              "name": "snackbar",
              "type": "link"
            },
            {
              "route": "tooltip",
              "name": "tooltip",
              "type": "link"
            }
          ]
        },
        {
          "route": "data-table",
          "name": "data-table",
          "type": "sub",
          "children": [
            {
              "route": "paginator",
              "name": "paginator",
              "type": "link"
            },
            {
              "route": "sort",
              "name": "sort",
              "type": "link"
            },
            {
              "route": "table",
              "name": "table",
              "type": "link"
            }
          ]
        }
      ],
      "permissions": {
        "except": [
          "MANAGER",
          "GUEST"
        ]
      }
    },
    {
      "route": "permissions",
      "name": "permissions",
      "type": "sub",
      "icon": "lock",
      "children": [
        {
          "route": "role-switching",
          "name": "role-switching",
          "type": "link"
        },
        {
          "route": "route-guard",
          "name": "route-guard",
          "type": "link",
          "permissions": {
            "except": "GUEST"
          }
        },
        {
          "route": "test",
          "name": "test",
          "type": "link",
          "permissions": {
            "only": "ADMIN"
          }
        }
      ]
    },
    {
      "route": "media",
      "name": "media",
      "type": "sub",
      "icon": "image",
      "children": [
        {
          "route": "gallery",
          "name": "gallery",
          "type": "link"
        }
      ]
    },
    {
      "route": "forms",
      "name": "forms",
      "type": "sub",
      "icon": "description",
      "children": [
        {
          "route": "elements",
          "name": "form-elements",
          "type": "link"
        },
        {
          "route": "dynamic",
          "name": "dynamic-form",
          "type": "link"
        },
        {
          "route": "select",
          "name": "select",
          "type": "link"
        },
        {
          "route": "datetime",
          "name": "datetime",
          "type": "link"
        }
      ],
      "permissions": {
        "except": "GUEST"
      }
    },
    {
      "route": "tables",
      "name": "tables",
      "type": "sub",
      "icon": "format_line_spacing",
      "children": [
        {
          "route": "kitchen-sink",
          "name": "kitchen-sink",
          "type": "link"
        },
        {
          "route": "remote-data",
          "name": "remote-data",
          "type": "link"
        }
      ],
      "permissions": {
        "except": "GUEST"
      }
    },
    {
      "route": "profile",
      "name": "profile",
      "type": "sub",
      "icon": "person",
      "children": [
        {
          "route": "overview",
          "name": "overview",
          "type": "link"
        },
        {
          "route": "settings",
          "name": "settings",
          "type": "link"
        }
      ]
    },
    {
      "route": "https://ng-matero.github.io/extensions/",
      "name": "extensions",
      "type": "extTabLink",
      "icon": "extension",
      "permissions": {
        "only": "ADMIN"
      }
    },
    {
      "route": "/",
      "name": "sessions",
      "type": "sub",
      "icon": "question_answer",
      "children": [
        {
          "route": "403",
          "name": "403",
          "type": "link"
        },
        {
          "route": "404",
          "name": "404",
          "type": "link"
        },
        {
          "route": "500",
          "name": "500",
          "type": "link"
        }
      ],
      "permissions": {
        "only": "ADMIN"
      }
    },
    {
      "route": "utilities",
      "name": "utilities",
      "type": "sub",
      "icon": "all_inbox",
      "children": [
        {
          "route": "css-grid",
          "name": "css-grid",
          "type": "link"
        },
        {
          "route": "css-helpers",
          "name": "css-helpers",
          "type": "link"
        }
      ]
    },
    {
      "route": "menu-level",
      "name": "menu-level",
      "type": "sub",
      "icon": "subject",
      "children": [
        {
          "route": "level-1-1",
          "name": "level-1-1",
          "type": "sub",
          "children": [
            {
              "route": "level-2-1",
              "name": "level-2-1",
              "type": "sub",
              "children": [
                {
                  "route": "level-3-1",
                  "name": "level-3-1",
                  "type": "sub",
                  "children": [
                    {
                      "route": "level-4-1",
                      "name": "level-4-1",
                      "type": "link"
                    }
                  ]
                }
              ]
            },
            {
              "route": "level-2-2",
              "name": "level-2-2",
              "type": "link"
            }
          ]
        },
        {
          "route": "level-1-2",
          "name": "level-1-2",
          "type": "link"
        }
      ],
      "permissions": {
        "only": "ADMIN"
      }
    }
  ]
}
], status=status.HTTP_200_OK)
        elif request.user.is_member:
            return Response([{
  "menu": [
    {
      "route": "dashboard",
      "name": "dashboard",
      "type": "link",
      "icon": "dashboard",
      "badge": {
        "color": "red-50",
        "value": "5"
      }
    },
    {
      "route": "design",
      "name": "design",
      "type": "sub",
      "icon": "color_lens",
      "label": {
        "color": "azure-50",
        "value": "New"
      },
      "children": [
        {
          "route": "colors",
          "name": "colors",
          "type": "link",
          "icon": "colorize"
        },
        {
          "route": "icons",
          "name": "icons",
          "type": "link",
          "icon": "flag"
        }
      ],
      "permissions": {
        "only": [
          "ADMIN",
          "MANAGER"
        ]
      }
    },
    {
      "route": "material",
      "name": "material",
      "type": "sub",
      "icon": "favorite",
      "children": [
        {
          "route": "",
          "name": "form-controls",
          "type": "sub",
          "children": [
            {
              "route": "autocomplete",
              "name": "autocomplete",
              "type": "link"
            },
            {
              "route": "checkbox",
              "name": "checkbox",
              "type": "link"
            },
            {
              "route": "datepicker",
              "name": "datepicker",
              "type": "link"
            },
            {
              "route": "form-field",
              "name": "form-field",
              "type": "link"
            },
            {
              "route": "input",
              "name": "input",
              "type": "link"
            },
            {
              "route": "radio",
              "name": "radio",
              "type": "link"
            },
            {
              "route": "select",
              "name": "select",
              "type": "link"
            },
            {
              "route": "slider",
              "name": "slider",
              "type": "link"
            },
            {
              "route": "slide-toggle",
              "name": "slide-toggle",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "navigation",
          "type": "sub",
          "children": [
            {
              "route": "menu",
              "name": "menu",
              "type": "link"
            },
            {
              "route": "sidenav",
              "name": "sidenav",
              "type": "link"
            },
            {
              "route": "toolbar",
              "name": "toolbar",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "layout",
          "type": "sub",
          "children": [
            {
              "route": "card",
              "name": "card",
              "type": "link"
            },
            {
              "route": "divider",
              "name": "divider",
              "type": "link"
            },
            {
              "route": "expansion",
              "name": "expansion",
              "type": "link"
            },
            {
              "route": "grid-list",
              "name": "grid-list",
              "type": "link"
            },
            {
              "route": "list",
              "name": "list",
              "type": "link"
            },
            {
              "route": "stepper",
              "name": "stepper",
              "type": "link"
            },
            {
              "route": "tab",
              "name": "tab",
              "type": "link"
            },
            {
              "route": "tree",
              "name": "tree",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "buttons-indicators",
          "type": "sub",
          "children": [
            {
              "route": "button",
              "name": "button",
              "type": "link"
            },
            {
              "route": "button-toggle",
              "name": "button-toggle",
              "type": "link"
            },
            {
              "route": "badge",
              "name": "badge",
              "type": "link"
            },
            {
              "route": "chips",
              "name": "chips",
              "type": "link"
            },
            {
              "route": "icon",
              "name": "icon",
              "type": "link"
            },
            {
              "route": "progress-spinner",
              "name": "progress-spinner",
              "type": "link"
            },
            {
              "route": "progress-bar",
              "name": "progress-bar",
              "type": "link"
            },
            {
              "route": "ripple",
              "name": "ripple",
              "type": "link"
            }
          ]
        },
        {
          "route": "",
          "name": "popups-modals",
          "type": "sub",
          "children": [
            {
              "route": "bottom-sheet",
              "name": "bottom-sheet",
              "type": "link"
            },
            {
              "route": "dialog",
              "name": "dialog",
              "type": "link"
            },
            {
              "route": "snack-bar",
              "name": "snackbar",
              "type": "link"
            },
            {
              "route": "tooltip",
              "name": "tooltip",
              "type": "link"
            }
          ]
        },
        {
          "route": "data-table",
          "name": "data-table",
          "type": "sub",
          "children": [
            {
              "route": "paginator",
              "name": "paginator",
              "type": "link"
            },
            {
              "route": "sort",
              "name": "sort",
              "type": "link"
            },
            {
              "route": "table",
              "name": "table",
              "type": "link"
            }
          ]
        }
      ],
      "permissions": {
        "except": [
          "MANAGER",
          "GUEST"
        ]
      }
    },
    {
      "route": "permissions",
      "name": "permissions",
      "type": "sub",
      "icon": "lock",
      "children": [
        {
          "route": "role-switching",
          "name": "role-switching",
          "type": "link"
        },
        {
          "route": "route-guard",
          "name": "route-guard",
          "type": "link",
          "permissions": {
            "except": "GUEST"
          }
        },
        {
          "route": "test",
          "name": "test",
          "type": "link",
          "permissions": {
            "only": "ADMIN"
          }
        }
      ]
    },
    {
      "route": "media",
      "name": "media",
      "type": "sub",
      "icon": "image",
      "children": [
        {
          "route": "gallery",
          "name": "gallery",
          "type": "link"
        }
      ]
    },
    {
      "route": "forms",
      "name": "forms",
      "type": "sub",
      "icon": "description",
      "children": [
        {
          "route": "elements",
          "name": "form-elements",
          "type": "link"
        },
        {
          "route": "dynamic",
          "name": "dynamic-form",
          "type": "link"
        },
        {
          "route": "select",
          "name": "select",
          "type": "link"
        },
        {
          "route": "datetime",
          "name": "datetime",
          "type": "link"
        }
      ],
      "permissions": {
        "except": "GUEST"
      }
    },
    {
      "route": "tables",
      "name": "tables",
      "type": "sub",
      "icon": "format_line_spacing",
      "children": [
        {
          "route": "kitchen-sink",
          "name": "kitchen-sink",
          "type": "link"
        },
        {
          "route": "remote-data",
          "name": "remote-data",
          "type": "link"
        }
      ],
      "permissions": {
        "except": "GUEST"
      }
    },
    {
      "route": "profile",
      "name": "profile",
      "type": "sub",
      "icon": "person",
      "children": [
        {
          "route": "overview",
          "name": "overview",
          "type": "link"
        },
        {
          "route": "settings",
          "name": "settings",
          "type": "link"
        }
      ]
    },
    {
      "route": "https://ng-matero.github.io/extensions/",
      "name": "extensions",
      "type": "extTabLink",
      "icon": "extension",
      "permissions": {
        "only": "ADMIN"
      }
    },
    {
      "route": "/",
      "name": "sessions",
      "type": "sub",
      "icon": "question_answer",
      "children": [
        {
          "route": "403",
          "name": "403",
          "type": "link"
        },
        {
          "route": "404",
          "name": "404",
          "type": "link"
        },
        {
          "route": "500",
          "name": "500",
          "type": "link"
        }
      ],
      "permissions": {
        "only": "ADMIN"
      }
    },
    {
      "route": "utilities",
      "name": "utilities",
      "type": "sub",
      "icon": "all_inbox",
      "children": [
        {
          "route": "css-grid",
          "name": "css-grid",
          "type": "link"
        },
        {
          "route": "css-helpers",
          "name": "css-helpers",
          "type": "link"
        }
      ]
    },
    {
      "route": "menu-level",
      "name": "menu-level",
      "type": "sub",
      "icon": "subject",
      "children": [
        {
          "route": "level-1-1",
          "name": "level-1-1",
          "type": "sub",
          "children": [
            {
              "route": "level-2-1",
              "name": "level-2-1",
              "type": "sub",
              "children": [
                {
                  "route": "level-3-1",
                  "name": "level-3-1",
                  "type": "sub",
                  "children": [
                    {
                      "route": "level-4-1",
                      "name": "level-4-1",
                      "type": "link"
                    }
                  ]
                }
              ]
            },
            {
              "route": "level-2-2",
              "name": "level-2-2",
              "type": "link"
            }
          ]
        },
        {
          "route": "level-1-2",
          "name": "level-1-2",
          "type": "link"
        }
      ],
      "permissions": {
        "only": "ADMIN"
      }
    }
  ]
}
], status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)


class MyTasks(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Retrieve all tasks assigned to the current user.
        """
        my_tasks = Q(assigned_user=request.user)
        active_tasks = Q(status__active_state=True)
        tasks = Task.objects.filter(my_tasks & active_tasks)

        if not tasks.exists():
            return Response([], status=status.HTTP_204_NO_CONTENT)
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# TODO: Task Serializer with audit info

# TODO: All Users availability
# TODO: User availability get
# TODO: User availability create
# TODO: User availability update
# TODO: User availability delete