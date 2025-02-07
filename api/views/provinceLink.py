from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.models.Link import Link
from api.models.Role import Role
from api.models.Province import Province
from api.serializers.LinkSerializer import LinkSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status




@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def provinceLinks(request, link_id=None):
    """
    Handles all operations (GET, POST, PUT, PATCH, DELETE) for province links.
    """
    logged_in_user = request.user

    # Ensure the user has the required role
    if logged_in_user.role.role_name != Role.PROVINCIAL_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Retrieve all links for the logged-in user's province
        province_links = Link.objects.filter(province=logged_in_user.province)
        return Response({'province_links': list(province_links.values())}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Create a new link
        link_serializer = LinkSerializer(data=request.data)
        if link_serializer.is_valid():
            province_id_from_request = request.data.get('province')
            if str(province_id_from_request) != str(logged_in_user.province.provinceCode):
                return Response({"detail": "You can only create links for your assigned province."},
                                status=status.HTTP_403_FORBIDDEN)
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_201_CREATED)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        # Update an existing link
        if not link_id:
            return Response({"detail": "Link ID is required for updating."}, status=status.HTTP_400_BAD_REQUEST)

        link = get_object_or_404(Link, linkId=link_id, province=logged_in_user.province)
        link_serializer = LinkSerializer(link, data=request.data, partial=(request.method == 'PATCH'))
        if link_serializer.is_valid():
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_200_OK)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete an existing link
        if not link_id:
            return Response({"detail": "Link ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)

        link = get_object_or_404(Link, linkId=link_id, province=logged_in_user.province)
        link.delete()
        return Response({'detail': 'Link deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
