from rest_framework import serializers

from api.models import LG

class LgSerializer(serializers.ModelSerializer):
    class Meta:
        model = LG
        fields = '__all__'