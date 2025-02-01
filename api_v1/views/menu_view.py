from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import views

from api_v1.permissions import IsActiveUser


class MenuView(views.APIView):
    permission_classes = [IsActiveUser]

    def get(self, request: Request) -> Response:
        """
        Retrieve the current user's menu.
        """
        from core.menu import menu
        # TODO: Add badges values
        return Response(menu, status=status.HTTP_200_OK)
