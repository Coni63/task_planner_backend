from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from .base_view import BaseAuthenticatedView


class MenuView(BaseAuthenticatedView):
    def get(self, request: Request) -> Response:
        """
        Retrieve the current user's menu.
        """
        if not request.user.is_active:
            return Response([], status=status.HTTP_200_OK)

        from core.menu import menu
        # TODO: Add badges values
        return Response(menu, status=status.HTTP_200_OK)
