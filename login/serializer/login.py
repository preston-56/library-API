from rest_framework import serializers
from login.models.login import Login
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        user = User.objects.filter(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            return {"user": user}
        raise serializers.ValidationError("Invalid username or password")

    def create(self, validated_data):
        user = validated_data["user"]
        # Record login attempt in the Login model
        Login.objects.create(user=user)
        return user
