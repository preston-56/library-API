from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from authors.models.authors import Author
from authors.serializers.author import AuthorSerializer
from drf_yasg.utils import swagger_auto_schema

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description="Retrieve a list of all authors")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
