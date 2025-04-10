from rest_framework import serializers
from books.models.book import Book
from favorite.models.books import Favorite
from books.serializers.book import BookSerializer
class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'book']

    def create(self, validated_data):
        book_data = validated_data.pop('book')
        book, created = Book.objects.get_or_create(
            title=book_data['title'],
            author__name=book_data['author']['name'],  # Ensure the author exists
            defaults=book_data
        )
        favorite = Favorite.objects.create(book=book, **validated_data)
        return favorite
