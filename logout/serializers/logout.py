from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from blacklist.models.blacklist import Blacklist

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get('refresh_token')
        try:
            # Validate the refresh token using the simplejwt library
            RefreshToken(refresh_token)
        except Exception as e:
            raise serializers.ValidationError("Invalid token") from e

        return data

    def save(self):
        refresh_token = self.validated_data["refresh_token"]
        # Store the refresh token in the Blacklist model
        Blacklist.objects.create(token=refresh_token)
