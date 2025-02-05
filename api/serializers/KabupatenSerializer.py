from rest_framework import serializers
from api.serializers.ProvinceSerializer import ProvinceSerializer
from api.models.kabupaten import Kabupaten

class KabupatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kabupaten
        fields = '__all__'