from typing import Type
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from django.db.models import Model

from task_manager.permissions import CustomJWTAuthentication, IsActiveUser, IsAdminUser


class BaseAuthenticatedView(APIView):
    """
    A base view class for views where GET requests are accessible to all
    authenticated users, but other requests are restricted to admin users.
    """
    authentication_classes = [CustomJWTAuthentication]
    base_serializer_class: Type[BaseSerializer] = None
    base_model_class: Type[Model] = None

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsActiveUser()]
        else:
            return [IsAdminUser()]

    def get_list(self):
        """
        Retrieve all objects.
        """
        objects = self.base_model_class.objects.all()
        if not objects.exists():
            Response([], status=status.HTTP_200_OK)

        serializer = self.base_serializer_class(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_object(self, object_id):
        """
        Retrieve a single object by ID.
        """
        try:
            object = self.base_model_class.objects.get(pk=object_id)
        except self.base_model_class.DoesNotExist:
            raise NotFound(detail=f"{self.base_model_class.__name__} not found")

        serializer = self.base_serializer_class(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_object(self, data):
        """
        Create a new object.
        """
        serializer = self.base_serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_object(self, object_id, data):
        """
        Update an object by ID.
        """
        return self.__inner_update_object(object_id, data, False)

    def patch_object(self, object_id, data):
        """
        Partially update an object by ID.
        """
        return self.__inner_update_object(object_id, data, True)
    
    def __inner_update_object(self, object_id, data, partial):
        """
        Update an object instance.
        """
        try:
            object = self.base_model_class.objects.get(pk=object_id)
        except self.base_model_class.DoesNotExist:
            raise NotFound(detail=f"{self.base_model_class.__name__} not found")

        serializer = self.base_serializer_class(object, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete_object(self, object_id):
        """
        Delete an object by ID.
        """
        try:
            object = self.base_model_class.objects.get(pk=object_id)
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except self.base_model_class.DoesNotExist:
            raise NotFound(detail=f"{self.base_model_class.__name__} not found")