from rest_framework import serializers
from api.models.roadInventory import RoadInventory

class RoadInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadInventory
        fields = '__all__'
