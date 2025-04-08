from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from authors.models.authors import Author
from authors.serializers.author import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
