import datetime
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        expires_in = int(access_token_lifetime.total_seconds())

        decoded_token = jwt.decode(
            data.get("access"), 
            options={"verify_signature": False}  # On ne vérifie pas la signature
        )
        exp = decoded_token.get("exp")  # Date d'expiration du token

        custom_response = {
            "access_token": data.get("access"),
            "refresh_token": data.get("refresh"),
            "token_type": "Bearer",
            "expires_in": expires_in,
            "exp": exp,
        }
        
        return Response(custom_response)
    



class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        access_token = data.get("access")

        # Decode the access token (without signature verification)
        decoded_token = jwt.decode(
            access_token, 
            options={"verify_signature": False}  # Do not verify the signature
        )

        exp = decoded_token.get("exp")  # Get expiration timestamp

        custom_response = {
            "access_token": access_token,
            "refresh_token": request.data.get("refresh"),  # Use the same refresh token from request
            "token_type": "Bearer",
            "expires_in": exp - int(datetime.datetime.now().timestamp()),  # Calculate remaining time
            "exp": exp,  # Expiration timestamp
            **{key: value for key, value in data.items() if key != "access"}  # Include any other fields
        }
        
        return Response(custom_response)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=200)
        except Exception:
            return Response({"error": "Invalid token or logout failed."}, status=400)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active
        token['is_member'] = user.is_member
        token['is_admin'] = user.is_admin

        return token