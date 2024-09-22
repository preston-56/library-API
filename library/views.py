from rest_framework import viewsets, permissions, generics
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


from .models import Author, Book, Favorite
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    FavoriteSerializer,
    RegisterSerializer,
    LoginSerializer,
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, author_name):
        # Accessing request attributes
        author_id = Author.get_author_id(author_name)

        if author_id:
            return Response({"author_id": author_id})
        else:
            return Response({"error": "Author not found"}, status=404)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(author__name__icontains=search)
            )
        return queryset


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the data
        user = serializer.save()  # Create the user using the serializer

        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "user_id": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=201,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def post(self, request, *args, **kwargs):
        # Validate and authenticate user using the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user object from validated data
        user = serializer.validated_data["user"]

        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)

        # Return the tokens in the response
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=200,
        )


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get("refresh")

            # Check if the refresh token is provided
            if refresh_token is None:
                return Response({"error": "Refresh token is required."}, status=400)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.AllowAny]  # Ensure user is authenticated

    def create(self, request, *args, **kwargs):
        user = request.user

        # Ensure user is authenticated
        if not user.is_authenticated:
            return Response(
                {"error": "Authentication is required to add favorites."}, status=401
            )

        book_id = request.data.get("book_id")

        # Limit to 20 favorites
        if Favorite.objects.filter(user=user).count() >= 20:
            return Response(
                {"error": "Maximum of 20 favorite books allowed."}, status=400
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        favorite, created = Favorite.objects.get_or_create(user=user, book=book)
        if not created:
            return Response(
                {"error": "This book is already in your favorites."}, status=400
            )

        # Get recommendations
        recommendations = self.get_recommendations(user)

        return Response(
            {
                "message": "Favorite added successfully.",
                "favorite": FavoriteSerializer(favorite).data,
                "recommendations": BookSerializer(recommendations, many=True).data,
            }
        )

    def get_recommendations(self, user):
        # Get the user's favorite books
        favorite_books = Favorite.objects.filter(user=user).values_list(
            "book", flat=True
        )

        # If there are no favorites, return an empty list
        if not favorite_books:
            return []

        # Example Recommendation Logic: Recommend books by the same author
        recommended_books = (
            Book.objects.filter(
                author__in=Book.objects.filter(id__in=favorite_books).values_list(
                    "author", flat=True
                )
            )
            .exclude(id__in=favorite_books)  # Exclude books already favorited
            .distinct()[:5]  # Limit to 5 recommendations
        )

        return recommended_books
