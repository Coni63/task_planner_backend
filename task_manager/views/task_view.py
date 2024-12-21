import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from django.db.models import Q, F

from task_manager.models import Status, Task, UserAssignment
from task_manager.serializers import SearchRequestModelSerializer, TaskOrderSerializer, TaskSerializer, TaskSimpleSerializer
from task_manager.views.base_view import BaseAuthenticatedView


class TaskList(BaseAuthenticatedView):
    input_serializer_class = TaskSimpleSerializer
    output_serializer_class = TaskSerializer
    base_model_class = Task

    def get(self, request: Request) -> Response:
        """
        Retrieve all tasks or for a single project (by id with query param 'project')
        """
        my_tasks = request.query_params.get("me")
        project_id = request.query_params.get("project")
        statuses = request.query_params.getlist("states", [])

        tasks = Task.objects.all()
        if my_tasks:
            tasks = tasks.filter(picked_by=request.user)
        if project_id:
            tasks = tasks.filter(project = project_id)
        if statuses:
            tasks = tasks.filter(status__state__in=statuses)

        if not tasks.exists():
            return Response([], status=status.HTTP_200_OK)

        tasks = tasks.order_by(F('order').asc(nulls_last=True), 'created_at')

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Create a new task.
        """
        return self.create_object(request.data)


class TaskDetail(BaseAuthenticatedView):
    input_serializer_class = TaskSimpleSerializer
    output_serializer_class = TaskSerializer
    base_model_class = Task

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

    def delete(self, request: Request, task_id: str) -> Response:
        """
        Delete a task by ID.
        """
        return self.delete_object(task_id)

    def put(self, request: Request, task_id: str) -> Response:
        """
        Update a task by ID.
        """
        return self.update_object(task_id, request.data)
    
    def patch(self, request, task_id: str) -> Response:
        """
        Partially update a task by ID.
        """
        return self.patch_object(task_id, request.data)


class TaskPickView(BaseAuthenticatedView):

    def get(self, request: Request) -> Response:

        if Task.objects.filter(picked_by=request.user).filter(status__state='active').exists():
            return Response({"error": "User already has an active task"}, status=status.HTTP_412_PRECONDITION_FAILED)

        my_categories = UserAssignment.objects.filter(user=request.user).filter(~Q(level="Blocked")).values_list('category', flat=True)

        next_task = Task.objects.filter(category__in=my_categories).filter(status__state='pending').order_by('order').first()

        if not next_task:
            return Response(status=status.HTTP_200_OK)
        
        next_task.picked_by = request.user
        next_task.picked_at = datetime.datetime.now(datetime.timezone.utc)
        next_task.status = Status.objects.get(status='In Progress')
        next_task.save()

        serializer = TaskSerializer(next_task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TaskListView(BaseAuthenticatedView):
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
    


class TaskOrderView(BaseAuthenticatedView):
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
