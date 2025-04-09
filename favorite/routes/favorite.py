from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from favorite.models.books import Favorite, Book
from favorite.serializers.favorite import FavoriteSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        # Ensure the user who is creating the favorite is the logged-in user
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Get up to 5 recommended books based on your favorites. "
                              "Recommendations are books by the same authors.",
        responses={
            200: openapi.Response(
                description="A list of recommended books",
                schema=FavoriteSerializer(many=True)
            ),
            400: openapi.Response(
                description="No favorite books found"
            ),
        },
    )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommendations(self, request):
        """
        Get up to 5 recommended books based on the user's favorite books.
        This is a basic recommendation system that suggests books by the same author.
        """
        user = request.user

        # Get the books the user has favorited
        favorites = Favorite.objects.filter(user=user).select_related('book')

        if not favorites:
            return Response({"message": "No favorite books found"}, status=400)

        # Get the authors of the user's favorite books
        favorite_authors = favorites.values_list('book__author', flat=True).distinct()

        # Find other books by the same authors
        recommended_books = Book.objects.filter(author__in=favorite_authors).exclude(
            id__in=[fav.book.id for fav in favorites]
        ).distinct()

        # Limit to 5 recommendations
        recommended_books = recommended_books[:5]

        # Serialize the recommended books
        recommended_books_serializer = FavoriteSerializer(recommended_books, many=True)

        return Response(recommended_books_serializer.data)

