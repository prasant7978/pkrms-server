from rest_framework import serializers

from api.models import Kabupaten

class KabupatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kabupaten
        fields = '__all__'