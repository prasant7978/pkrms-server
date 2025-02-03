from rest_framework import viewsets
from api.models.Province import Province
from api.serializers.ProvinceSerializer import ProvinceSerializer

class ProvinceView(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer