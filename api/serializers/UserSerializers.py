from rest_framework import serializers
from api.serializers.RoleSerializer import RoleSerializer
from api.models.User import User ,ApprovalRequest
from api.models.Province import Province
from api.models.Balai import Balai
from api.models.Role import Role
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    province = serializers.StringRelatedField()  # If you want just the name, use `StringRelatedField()`
    Kabupaten = serializers.StringRelatedField()
    balai = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name', 'is_active', 'is_staff', 'date_joined', 'approved', 'role', 'province', 'Kabupaten', 'balai']


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(max_length=50)
    balai = serializers.CharField()
    province = serializers.IntegerField()
    kabupaten = serializers.IntegerField(required=False)



class ApprovalRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    approver = UserSerializer(read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = ['user', 'approver', 'created_at', 'status']