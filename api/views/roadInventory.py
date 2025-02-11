
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from api.models.roadInventory import RoadInventory 
from api.models.Province import Province
from api.models.Link import Link
from api.serializers.RoadInventorySerializer import RoadInventorySerializer
from api.serializers.LinkSerializer import LinkSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models.Role import Role

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def roadInventory(request, roadInventoryId=None):
    """
    Handle listing, creating, retrieving, updating, and deleting RoadInventory items
    for links under the user's province.
    """
    logged_in_user = request.user

    # Ensure the user has the required role
    if logged_in_user.role.role_name != Role.PROVINCIAL_LG:
        return Response({'detail': 'Unauthorized access.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        link_id = request.GET.get('linkId')  # Get linkId from query parameters

        if link_id:
            # Fetch the link and ensure it belongs to the logged-in user's province
            link = get_object_or_404(Link, linkId=link_id, province=logged_in_user.province)
            road_inventory = RoadInventory.objects.filter(linkId=link)
        else:
            # If no linkId is provided, fetch road inventory for all links under the user's province
            road_inventory_links = Link.objects.filter(province=logged_in_user.province)
            road_inventory = RoadInventory.objects.filter(linkId__in=road_inventory_links)

        serializer = RoadInventorySerializer(road_inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        link_id = request.data.get('linkId')
        link = get_object_or_404(Link, linkId=link_id)

        if link.province != logged_in_user.province:
            return Response({'detail': 'Unauthorized to add data for this link.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = RoadInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        road_inventory = get_object_or_404(RoadInventory, roadInventoryId=roadInventoryId)
        if road_inventory.linkId.province != logged_in_user.province:
            return Response({'detail': 'Unauthorized access.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = RoadInventorySerializer(road_inventory, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        road_inventory = get_object_or_404(RoadInventory, roadInventoryId=roadInventoryId)
        if road_inventory.linkId.province != logged_in_user.province:
            return Response({'detail': 'Unauthorized access.'}, status=status.HTTP_403_FORBIDDEN)
        
        road_inventory.delete()
        return Response({'detail': 'RoadInventory entry deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
