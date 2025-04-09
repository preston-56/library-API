from rest_framework import serializers
from books.models.book import Book
from authors.serializers.author import AuthorSerializer

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_date']
