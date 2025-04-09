from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from login.serializer.login import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login user and receive JWT tokens.",
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "message": "Welcome back, <username>"
                    }
                }
            ),
            400: "Validation error"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # Generate tokens or any post-login logic here

        return Response({"message": f"Welcome back, {user.username}"})
