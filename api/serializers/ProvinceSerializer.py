from rest_framework import serializers

from api.models.province import Province

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'