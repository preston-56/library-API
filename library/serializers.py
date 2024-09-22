from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import Author, Book, Favorite, User
from django.contrib.auth import authenticate


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

def create(self, validated_data):
    author_name = validated_data.pop('author_name', None)
    if author_name is None:
        raise serializers.ValidationError("Author name is required.")
    
    author_id = Author.get_author_id(author_name)
    if author_id is None:
        raise serializers.ValidationError("Author not found.")
    
    # Check for existing book with the same title and author_id
    existing_book = Book.objects.filter(title=validated_data['title'], author_id=author_id).first()
    if existing_book:
        raise serializers.ValidationError("This book already exists for the given author.")
    
    book = Book.objects.create(author_id=author_id, **validated_data)
    return book


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']

    def create(self, validated_data):
        # The author field should already be a primary key due to the PrimaryKeyRelatedField
        book = Book.objects.create(**validated_data)
        return book


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print("Attempting to authenticate:", data)
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid login credentials.")
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Attach user object to data
        data['user'] = user
        data['refresh'] = str(refresh)  # Convert to string
        data['access'] = str(refresh.access_token)  # Get access token
        
        return data