from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from logout.serializers.logout import LogoutSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from blacklist.models import Blacklist 

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Logs out a user by invalidating their refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='The refresh token to invalidate'),
            },
            required=['refresh_token']
        ),
        responses={
            200: openapi.Response(
                description="Logged out successfully",
                examples={
                    "application/json": {
                        "message": "Logged out successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid refresh token provided"
            ),
            404: openapi.Response(
                description="Token not found"
            )
        }
    )
    def post(self, request, *args, **kwargs):
        # Validate the provided refresh token using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get('refresh_token')

        # Blacklist the refresh token
        try:
            # Create a RefreshToken instance and blacklist it
            token = RefreshToken(refresh_token)
            Blacklist.objects.create(token=str(token))

            return Response({"message": "Logged out successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

