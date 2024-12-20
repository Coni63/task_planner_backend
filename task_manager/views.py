import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField

from .permissions import CustomJWTAuthentication, IsAdminUser
from .models import Category, Project, Status, Task, CustomUser, UserAssignment
from .serializers import (
    CategorySerializer,
    ProjectSerializer,
    SearchRequestModelSerializer,
    StatusSerializer,
    TaskOrderSerializer,
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
        users = CustomUser.objects.prefetch_related('categories').all()
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
    
    def post(self, request: Request) -> Response:
        """
        Create a new category.
        """
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request: Request, category_id: str) -> Response:
        """
        Delete a category by ID.
        """
        try:
            category = Category.objects.get(pk=category_id)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            raise NotFound(detail="Category not found")
        
    def put(self, request: Request, category_id: str) -> Response:
        """
        Update a category by ID.
        """
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise NotFound(detail="Category not found")

        serializer = CategorySerializer(category, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
    
    def post(self, request: Request) -> Response:
        """
        Create a new status.
        """
        serializer = StatusSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def delete(self, request: Request, status_id: str) -> Response:
        """
        Delete a status by ID.
        """
        try:
            record = Status.objects.get(pk=status_id)
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Status.DoesNotExist:
            raise NotFound(detail="Status not found")

    def put(self, request: Request, status_id: str) -> Response:
        """
        Update a status by ID.
        """
        try:
            record = Status.objects.get(pk=status_id)
        except Status.DoesNotExist:
            raise NotFound(detail="Status not found")

        serializer = StatusSerializer(record, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskList(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        """
        Retrieve all tasks or for a single project (by id with query param 'project')
        """
        project_id = request.query_params.get("project")

        open_tasks = ~Q(status__state = "closed")

        if project_id:
            for_project = Q(project = project_id)

            tasks = Task.objects.filter(open_tasks & for_project).annotate(
                order_nulls_last=Case(
                    When(order=None, then=Value(float('inf'))),  # None becomes "infinity"
                    default='order',
                    output_field=IntegerField()
                )
            ).order_by('order_nulls_last', 'created_at')
            if not tasks.exists():
                return Response([], status=status.HTTP_204_NO_CONTENT)
        else:
            tasks = Task.objects.filter(open_tasks).annotate(
                order_nulls_last=Case(
                    When(order=None, then=Value(float('inf'))),  # None becomes "infinity"
                    default='order',
                    output_field=IntegerField()
                )
            ).order_by('order_nulls_last', 'created_at')
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
    
    def patch(self, request, *args, **kwargs):
        # Extract the ID from the URL or request body
        task_id = kwargs.get('id') or request.data.get('id')
        
        # Validate that the task exists
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Pass the instance to the serializer for partial update
        serializer = TaskSimpleSerializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskPickView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:

        if Task.objects.filter(picked_by=request.user).filter(status__state='active').exists():
            return Response({"error": "User already has an active task"}, status=status.HTTP_412_PRECONDITION_FAILED)

        my_categories = UserAssignment.objects.filter(user=request.user).filter(~Q(level="Blocked")).values_list('category', flat=True)

        next_task = Task.objects.filter(category__in=my_categories).filter(status__state='pending').order_by('order').first()

        if not next_task:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        next_task.picked_by = request.user
        next_task.picked_at = datetime.datetime.now(datetime.timezone.utc)
        next_task.status = Status.objects.get(status='In Progress')
        next_task.save()

        serializer = TaskSerializer(next_task)
        return Response(serializer.data, status=status.HTTP_200_OK)



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

        from .menu import menu
        # TODO: Add badges values
        return Response(menu, status=status.HTTP_200_OK)


class MyTasks(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Retrieve all tasks assigned to the current user.
        """
        my_tasks = Q(picked_by=request.user)
        active_tasks = Q(status__state='active')
        tasks = Task.objects.filter(my_tasks & active_tasks)

        if not tasks.exists():
            return Response([], status=status.HTTP_204_NO_CONTENT)
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskListView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SearchRequestModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        
        query_base = Task.objects.filter(status__state='closed')
        
        # Filtering based on individual column search
        for col in params['columns']:
            if col['searchable'] and col['search']['value']:
                lookup = {f"{col['data']}__icontains": col['search']['value']}
                query_base = query_base.filter(**lookup)
                
        # Global search across all searchable columns
        if params.get('search') and params['search']['value']:
            search_filters = Q()
            for col in params['columns']:
                if col['searchable']:
                    search_filters |= Q(**{f"{col['data']}__icontains": params['search']['value']})
            query_base = query_base.filter(search_filters)
        
        # Ordering
        for order in params['order']:
            col = params['columns'][order['column']]
            if col['orderable']:
                direction = '' if order['dir'] == 'asc' else '-'
                query_base = query_base.order_by(f"{direction}{col['data']}")
        
        # Count total and filtered records
        total = Task.objects.count()
        filtered = query_base.count()
        
        # Pagination
        if params.get('length') is not None:
            query_base = query_base[params['start']:params['start'] + params['length']]
        
        items = TaskSerializer(query_base, many=True).data
        
        response_data = {
            'items': items,
            'total': total,
            'filtered': filtered,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class TaskOrderView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        # Validate incoming data
        serializer = TaskOrderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        
        # Reset all task orders to null
        Task.objects.update(order=None)  # Resets the order field for all tasks

        # Update only the provided tasks with their new order
        tasks_to_update = []
        for task_data in serializer.validated_data:
            task = Task.objects.get(pk=task_data['id'])
            if task:
                task.order = task_data['order']
                tasks_to_update.append(task)
        
        # Bulk update to minimize queries
        Task.objects.bulk_update(tasks_to_update, ['order'])

        return Response({'message': 'Task order updated successfully'}, status=status.HTTP_200_OK)


# TODO: All Users availability
# TODO: User availability get
# TODO: User availability create
# TODO: User availability update
# TODO: User availability delete

# TODO: RememberMe