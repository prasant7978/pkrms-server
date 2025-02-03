from rest_framework import serializers

from api.models import PFID

class PfidSerializer(serializers.ModelSerializer):
    class Meta:
        model = PFID
        fields = '__all__'