from rest_framework import serializers
from api.serializers.RoleSerializer import RoleSerializer
from api.models.User import User ,ApprovalRequest
from api.models.Province import Province
from api.models.Balai import Balai
from api.models.Role import Role
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    province = serializers.CharField(source='province.provinceName', read_only=True)  
    Kabupaten = serializers.CharField(source='Kabupaten.KabupatenName', read_only=True)
    balai = serializers.CharField(source='balai.balaiName', read_only=True)  # Correct field reference

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'date_joined', 'approved', 'role', 'province', 'Kabupaten', 'balai']



class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    phone_number = serializers.CharField(
        max_length=15,
        required=False,
        allow_null=True,
        allow_blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+62\d{9,13}$',
                message="Phone number must be in Indonesian format, starting with +62 followed by 9 to 13 digits."
            )
        ]
    )
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