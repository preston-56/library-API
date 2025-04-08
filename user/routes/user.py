from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from user.serializers.user import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

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
