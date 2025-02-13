
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
def roadInventory(request):
    """
    Handles listing, creating, updating, and deleting RoadInventory items
    using linkId passed in the request body or query parameters.
    """
    logged_in_user = request.user

    # Ensure the user has the required role
    # if logged_in_user.role.role_name != Role.PROVINCIAL_LG:
    #     return Response({'detail': 'Unauthorized access.'}, status=status.HTTP_403_FORBIDDEN)

    # Fetch `linkId` from request data or query parameters
    # print(logged_in_user.province.provinceCode)
    # print(logged_in_user.Kabupaten.KabupatenCode)
    link_id = f"{logged_in_user.province.provinceCode}-{logged_in_user.Kabupaten.KabupatenCode}-{request.data.get('linkId') or request.GET.get('linkId')}"
    print(link_id)
    
    # formatted_link_id = f"{logged_in_user.province.provinceCode}-{logged_in_user.Kabupaten.KabupatenCode}-{request.data.get('linkId') or request.GET.get('linkId')}"
    # print(formatted_link_id)

    if not link_id:
        return Response({'detail': 'Link ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the Link and ensure it belongs to the logged-in user's province
    try:
        link = Link.objects.get(linkId=link_id)
    except Link.DoesNotExist:
        return Response({'detail': 'Invalid Link ID or unauthorized access.'}, status=status.HTTP_404_NOT_FOUND)

    #  Handle GET request (Fetch all road inventory for the given linkId)
    if request.method == 'GET':
        road_inventory = RoadInventory.objects.filter(linkId=link)
        serializer = RoadInventorySerializer(road_inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #  Handle POST request (Create new Road Inventory)
    elif request.method == 'POST':
        data = request.data.copy()
        data['linkId'] = link.linkId  # Ensure correct linkId is used
        serializer = RoadInventorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  Handle PUT/PATCH request (Update existing Road Inventory)
    elif request.method in ['PUT', 'PATCH']:
        try:
            road_inventory = RoadInventory.objects.get(linkId=link)
        except RoadInventory.DoesNotExist:
            return Response({'detail': 'RoadInventory entry not found for this linkId.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoadInventorySerializer(road_inventory, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  Handle DELETE request (Remove Road Inventory)
    elif request.method == 'DELETE':
        try:
            road_inventory = RoadInventory.objects.get(linkId=link)
            road_inventory.delete()
            return Response({'detail': 'RoadInventory entry deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except RoadInventory.DoesNotExist:
            return Response({'detail': 'RoadInventory entry not found for this linkId.'}, status=status.HTTP_404_NOT_FOUND)
