from rest_framework import serializers

from api.models.balai import Balai

class BalaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balai
        fields = '__all__'