from rest_framework import serializers

from api.models.User import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phoneNumber', 'is_active', 'is_staff']
