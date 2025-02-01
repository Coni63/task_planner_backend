from rest_framework import generics

from core.models import Category
from api_v1.permissions import CanCreateCategories, CanDeleteCategories, CanReadCategories, CanUpdateCategories
from api_v1.serializers import CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [CanReadCategories]
        elif self.request.method == 'POST':
            self.permission_classes = [CanCreateCategories]

        return super(CategoryList, self).get_permissions()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [CanReadCategories]
        elif self.request.method == 'DELETE':
            self.permission_classes = [CanDeleteCategories]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [CanUpdateCategories]

        return super(CategoryDetail, self).get_permissions()