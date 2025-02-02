from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Q
from api_v1.permissions import CanCreateTask, CanDeleteTask, CanPickTask, CanReadTask, CanUpdateTask
from core.models import Task, UserAssignment
from api_v1.serializers import SearchRequestModelSerializer, TaskSerializer, TaskSimpleSerializer
from django_filters import rest_framework as filters


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = ["project", "picked_by"]


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadTask]
        elif self.request.method == "POST":
            self.permission_classes = [CanCreateTask]

        return super(TaskList, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskSerializer
        elif self.request.method == "POST":
            return TaskSimpleSerializer

    def perform_create(self, serializer):
        task = Task.objects.create_task(**serializer.validated_data)
        serializer.instance = task  # Attach the created instance


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadTask]
        elif self.request.method == "DELETE":
            self.permission_classes = [CanDeleteTask]
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [CanUpdateTask]

        return super(TaskDetail, self).get_permissions()


class TaskPickView(views.APIView):
    """
    Event trigger when a user ask for a new task
    """

    authentication_classes = [CanPickTask]

    def get(self, request: Request) -> Response:
        if Task.objects.get_user_active_tasks(request.user).exists():
            return Response({"error": "User already has an active task"}, status=status.HTTP_412_PRECONDITION_FAILED)

        my_categories = UserAssignment.objects.get_user_assignments(request.user)
        next_task = Task.objects.pick_next_task(request.user, my_categories)

        if not next_task:
            return Response(status=status.HTTP_200_OK)

        return Response(TaskSerializer(next_task).data, status=status.HTTP_200_OK)


class TaskListView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = SearchRequestModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        query_base = Task.objects.filter(status__state="closed")

        # Filtering based on individual column search
        for col in params["columns"]:
            if col["searchable"] and col["search"]["value"]:
                lookup = {f"{col['data']}__icontains": col["search"]["value"]}
                query_base = query_base.filter(**lookup)

        # Global search across all searchable columns
        if params.get("search") and params["search"]["value"]:
            search_filters = Q()
            for col in params["columns"]:
                if col["searchable"]:
                    search_filters |= Q(**{f"{col['data']}__icontains": params["search"]["value"]})
            query_base = query_base.filter(search_filters)

        # Ordering
        for order in params["order"]:
            col = params["columns"][order["column"]]
            if col["orderable"]:
                direction = "" if order["dir"] == "asc" else "-"
                query_base = query_base.order_by(f"{direction}{col['data']}")

        # Count total and filtered records
        total = Task.objects.count()
        filtered = query_base.count()

        # Pagination
        if params.get("length") is not None:
            query_base = query_base[params["start"] : params["start"] + params["length"]]

        items = TaskSerializer(query_base, many=True).data

        response_data = {
            "items": items,
            "total": total,
            "filtered": filtered,
        }

        return Response(response_data, status=status.HTTP_200_OK)
