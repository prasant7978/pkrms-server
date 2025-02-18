from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.models.Link import Link
from api.serializers.LinkSerializer import LinkSerializer

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    
    @action(methods=['get'], detail=False)
    def getLinkByProvinceAndKabupaten(self, request, *args, **kwargs):
        # print('request.........', request)
        provinceId = request.query_params.get('provinceId', None)
        kabupatenId = request.query_params.get('kabupatenId', None)

        if provinceId and kabupatenId:
            links = self.queryset.filter(province=provinceId, kabupaten=kabupatenId)
        else:
            return Response({"error": "provinceId and kabupatenId are required."}, status=400)
        
        serialized_data = self.serializer_class(links, many=True)
        
        return Response({'province_links': serialized_data.data}, status=status.HTTP_200_OK)
        