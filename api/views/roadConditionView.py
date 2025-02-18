from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from api.models.roadCondition import RoadCondition
from api.models.roadInventory import RoadInventory 
from api.models.Province import Province
from api.models.Link import Link
from api.serializers.RoadConditionSerialiizers import RoadConditionSerializer
from api.serializers.RoadInventorySerializer import RoadInventorySerializer
from api.serializers.LinkSerializer import LinkSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models.Role import Role

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def roadConditionView(request):
    
    logged_in_user = request.user
    
    link_id = f"{request.data.get('province_id') or request.GET.get('province_id')}-{request.data.get('kabupaten_id') or request.GET.get('kabupaten_id')}-{request.data.get('linkId') or request.GET.get('linkId')}"
    year = request.data.get('year') or request.GET.get('year')
    if not link_id:
        return Response({'detail': 'Link ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        link = Link.objects.get(linkId=link_id)
    except Link.DoesNotExist:
        return Response({'detail': 'Invalid Link ID'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        road_condition = RoadCondition.objects.filter(linkId=link,year = year)
        serializer = RoadConditionSerializer(road_condition, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)