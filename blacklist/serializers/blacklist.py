from rest_framework import serializers
from blacklist.models.blacklist import Blacklist

class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = ['id', 'token', 'blacklisted_at']