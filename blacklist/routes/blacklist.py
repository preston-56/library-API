from rest_framework import viewsets
from blacklist.models import Blacklist
from blacklist.serializers.blacklist import BlacklistSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAdminUser

class BlacklistViewSet(viewsets.ModelViewSet):
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer
    permission_classes = [IsAdminUser]  # Optionally restrict access to admins

    @swagger_auto_schema(
        operation_description="Retrieve and manage blacklisted tokens.",
        responses={
            200: BlacklistSerializer(many=True),  
            401: openapi.Response(description="Unauthorized"),  # Unauthorized access
            404: openapi.Response(description="Not Found"),  # Data not found
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of blacklisted tokens.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new blacklisted token.",
        request_body=BlacklistSerializer,  # Body expects a Blacklist object
        responses={
            201: BlacklistSerializer,  # Successfully created a new blacklisted token
            400: openapi.Response(description="Bad Request")  # If invalid data is provided
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Add a new token to the blacklist.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific blacklisted token.",
        responses={
            200: BlacklistSerializer,  
            404: openapi.Response(description="Not Found")  
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific blacklisted token by ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific blacklisted token.",
        request_body=BlacklistSerializer,  # Expect a Blacklist object for updating
        responses={
            200: BlacklistSerializer,  
            400: openapi.Response(description="Bad Request"),  # Invalid request data
            404: openapi.Response(description="Not Found")  # Token not found
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update the details of a specific blacklisted token.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific blacklisted token.",
        responses={
            204: openapi.Response(description="Successfully deleted"), 
            404: openapi.Response(description="Not Found")  # Token not found
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a blacklisted token by ID.
        """
        return super().destroy(request, *args, **kwargs)
