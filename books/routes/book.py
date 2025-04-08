from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Q
from books.models.book import Book
from books.serializers.book import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(author__name__icontains=search)
            )
        return queryset
