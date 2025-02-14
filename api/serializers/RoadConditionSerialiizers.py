from rest_framework import serializers

from api.models.roadCondition import RoadCondition

class RoadConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadCondition
        fields = '__all__'
