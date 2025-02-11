from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework import status 
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import random
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models.Role import Role
from api.models.Link import Link
from api.models.Province import Province
from api.models.Kabupaten import Kabupaten
from api.models.User import User,ApprovalRequest
from api.models.Balai import Balai

#seializers
from api.serializers.LinkSerializer import LinkSerializer








@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def kabupatenLink(request):
    logged_in_user = request.user

    # Ensure the user has the required role
    if logged_in_user.role.role_name != Role.KABUPATEN_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Fetch links associated with the logged-in user's kabupaten
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
        response_data = {
            'kabupaten_links': list(kabupaten_links.values()),
        }
        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        action = request.data.get('action')
        if action == 'create_link':
            link_serializer = LinkSerializer(data=request.data)
            if link_serializer.is_valid():
                # Ensure the link is being created for the logged-in user's kabupaten
                if request.data.get('kabupaten') != str(logged_in_user.Kabupaten.KabupatenCode):
                    return Response(
                        {"detail": "You can only create links for your assigned kabupaten."},
                        status=status.HTTP_403_FORBIDDEN
                    )
                link_serializer.save()
                return Response(link_serializer.data, status=status.HTTP_201_CREATED)
            return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, linkId=link_id, kabupaten=logged_in_user.Kabupaten)
        
        link_serializer = LinkSerializer(link, data=request.data, partial=True)
        if link_serializer.is_valid():
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_200_OK)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        # PATCH method for partial updates of a link
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, linkId=link_id, kabupaten=logged_in_user.Kabupaten)
        
        link_serializer = LinkSerializer(link, data=request.data, partial=True)
        if link_serializer.is_valid():
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_200_OK)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, linkId=link_id, kabupaten=logged_in_user.Kabupaten)
        link.delete()
        return Response({'detail': 'Link deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
