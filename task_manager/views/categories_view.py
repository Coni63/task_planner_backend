from rest_framework.response import Response
from rest_framework.request import Request

from task_manager.models import Category
from task_manager.serializers import CategorySerializer
from task_manager.views.base_view import BaseAuthenticatedView



class CategoryList(BaseAuthenticatedView):
    input_serializer_class = CategorySerializer
    output_serializer_class = CategorySerializer
    base_model_class = Category

    def get(self, request: Request) -> Response:
        """
        Retrieve all categories.
        """
        return self.get_list()

    def post(self, request: Request) -> Response:
        """
        Create a new category.
        """
        return self.create_object(request.data)


class CategoryDetail(BaseAuthenticatedView):
    input_serializer_class = CategorySerializer
    output_serializer_class = CategorySerializer

    def delete(self, request: Request, category_id: str) -> Response:
        """
        Delete a category by ID.
        """
        return self.delete_object(category_id)
        
    def put(self, request: Request, category_id: str) -> Response:
        """
        Update a category by ID.
        """
        return self.update_object(category_id, request.data)
    