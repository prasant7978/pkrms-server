from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.models.Link import Link
from api.models.Role import Role
from api.models.Province import Province
from api.serializers.LinkSerializer import LinkSerializer
from api.models.Kabupaten import Kabupaten
from api.serializers.UserSerializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated










@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def provinceLinks(request, link_id=None):
    """
    Handles all operations (GET, POST, PUT, PATCH, DELETE) for province links.
    """
    logged_in_user = request.user
    print('req: ', request.user)

    # Ensure the user has the required role
    # if logged_in_user.role.role_name != Role.PROVINCIAL_LG:
    #     return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Retrieve all links for the logged-in user's province
        # Fetch all roles with their IDs
        roles = Role.objects.all().values('id', 'role_name')
        # print(roles)
        # print('kab: ', logged_in_user)
        # kabupaten_code=logged_in_user.Kabupaten.KabupatenCode
        # print('kab: ', kabupaten_code)

        # if logged_in_user.Kabupaten.KabupatenCode == "" or logged_in_user.Kabupaten.KabupatenCode == "0":
            
        province_links = Link.objects.filter(province=logged_in_user.province,kabupaten=logged_in_user.Kabupaten.KabupatenCode)
        logged_in_user_serializer = UserSerializer(logged_in_user)
        # print("ser data: ", logged_in_user_serializer.data)

        return Response({'province_links': list(province_links.values()), 'logged_in_user': logged_in_user_serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Ensure the user is only adding links for their assigned province
        province_code_from_request = request.data.get('province')

        if str(province_code_from_request) != str(logged_in_user.province.provinceCode):
            return Response({"detail": "You can only create links for your assigned province."},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate required fields
        required_fields = ['linkNo', 'kabupaten']
        for field in required_fields:
            if field not in request.data:
                return Response({field: "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract values
        link_no = request.data['linkNo']
        kabupaten_code = request.data['kabupaten']  # This should be the primary key

        # Retrieve province and kabupaten objects
        try:
            province = Province.objects.get(provinceCode=logged_in_user.province.provinceCode)
            kabupaten = Kabupaten.objects.get(KabupatenCode=kabupaten_code)
        except (Province.DoesNotExist, Kabupaten.DoesNotExist):
            return Response({"detail": "Invalid Province or Kabupaten Code."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the `linkId` using primary keys
        link_id_generated = f"{province.provinceCode}-{kabupaten.KabupatenCode}-{link_no}"

        # Create the link object
        link_data = request.data.copy()
        link_data['linkId'] = link_id_generated  # Assign generated linkId

        link_serializer = LinkSerializer(data=link_data)
        if link_serializer.is_valid():
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_201_CREATED)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        link_id = request.data.get('linkId')  # Extract linkId from request body
        print("Received link_id:", link_id)  # Debugging
        if not link_id:
          return Response({"detail": "Link ID is required for updating."}, status=status.HTTP_400_BAD_REQUEST)

        link = get_object_or_404(Link, linkId=link_id, province=logged_in_user.province)
        link_serializer = LinkSerializer(link, data=request.data, partial=(request.method == 'PATCH'))
        if link_serializer.is_valid():
           link_serializer.save()
           return Response(link_serializer.data, status=status.HTTP_200_OK)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        link_id = request.data.get('linkId')  # Extract linkId from request body
        print("Received link_id:", link_id)  # Debugging

        if not link_id:
           return Response({"detail": "Link ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)

        link = get_object_or_404(Link, linkId=link_id, province=logged_in_user.province)
        link.delete()

        return Response({'detail': 'Link deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
