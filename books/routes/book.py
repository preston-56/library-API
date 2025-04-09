from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from books.models.book import Book
from books.serializers.book import BookSerializer
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="List books. Optional `search` param to filter by title or author name.",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by book title or author name",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)

    def get_queryset(self):
            queryset = super().get_queryset()
            search = self.request.query_params.get("search", None)
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(author__name__icontains=search)
                )
            return queryset
