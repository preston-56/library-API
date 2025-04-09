from rest_framework import serializers
from favorite.models.books import Favorite
from books.serializers.book import BookSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'book']
