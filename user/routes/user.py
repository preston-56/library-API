from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from user.serializers.user import RegisterSerializer

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user and receive JWT tokens upon successful creation.",
        responses={
            201: openapi.Response(
                description="User created successfully",
                examples={
                    "application/json": {
                        "message": "User created successfully",
                        "user_id": 1,
                        "refresh": "your-refresh-token",
                        "access": "your-access-token"
                    }
                }
            ),
            400: "Validation error"
        }
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the data
        user = serializer.save()  # Create the user using the serializer

        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "user_id": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=201,
        )
