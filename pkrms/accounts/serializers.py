from rest_framework import serializers
from .models import Link,User,Role, DRP, LinkClass , RoadInventory, ConditionYear, RoadCondition , MCAcriteria

class LinkSerializer(serializers.ModelSerializer):
    province_code = serializers.CharField(source="province.code", read_only=True)
    kabupaten_code = serializers.CharField(source="kabupaten.code", read_only=True)

    class Meta:
        model = Link
        fields = [
            "id",
            "link_status",
            "link_number",
            "link_name",
            "link_function",
            "official_length_km",
            "actual_length_km",
            "highest_access",
            "province_code",
            "kabupaten_code",
        ]

class DRPSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRP
        fields = ['id', 'drp_number', 'chainage', 'drp_length', 'drp_type', 'drp_description', 'comment',
                  'gps_north_degree', 'gps_north_minute', 'gps_north_second',
                  'gps_east_degree', 'gps_east_minute', 'gps_east_second']


class LinkClassSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)
    kabupaten_name = serializers.CharField(source='kabupaten.name', read_only=True)
    link_name = serializers.CharField(source='link.link_name', read_only=True)
    
    # Explicit fields
    total_length = serializers.IntegerField()
    unit = serializers.CharField()
    
    class Meta:
        model = LinkClass
        fields = [
            'id',
            'province',
            'province_name',
            'kabupaten',
            'kabupaten_name',
            'link',
            'link_name',
            'total_length',
            'unit',
            'link_class',
        ]
from .models import LinkKabupaten, LinkKacematan

class LinkKabupatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkKabupaten
        fields = '__all__'


class LinkKacematanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkKacematan
        fields = '__all__'
   
class RoadInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadInventory
        fields = '__all__'
class ConditionYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionYear
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RoadConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadCondition
        fields = '__all__'


class MCAcriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCAcriteria
        fields = [
            'id',
            'link',
            'kabupaten',
            'province',
            'link_status',
            'link_number',
            'MCA_1',
            'MCA_2',
            'MCA_3',
            'MCA_4'
        ]
        read_only_fields = ['link_number']



from .models import Balai, Province, Kabupaten

class BalaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balai
        fields = ['id', 'name', 'balai_code']

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'balai', 'code', 'name', 'default_province', 'stable_network_objective']

class KabupatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kabupaten
        fields = ['id', 'province', 'balai', 'name', 'code', 'default_kabupaten', 'stable_network_objective']




from rest_framework import serializers
from .models import User, Role, Balai, Province, Kabupaten

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(max_length=50)
    balai = serializers.CharField(required=False)
    province = serializers.IntegerField(required=False)
    kabupaten = serializers.IntegerField(required=False)

class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)