from rest_framework import serializers
from api.models.link import Link

class LinkSerializer(serializers.ModelSerializer):
    province_code = serializers.CharField(source="province.code", read_only=True)
    kabupaten_code = serializers.CharField(source="kabupaten.code", read_only=True)

    class Meta:
        model = Link
        fields = "__all__"
