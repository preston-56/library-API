from rest_framework import serializers
from authors.models.authors import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'image_url', 'bio']
