from rest_framework import serializers
from api.models import BalaiLGMapping
class BalaiLgMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalaiLGMapping
        fields = '__all__'