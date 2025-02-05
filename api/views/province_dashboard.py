#modules 
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
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
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
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#models
from api.models.balai import Balai
from api.models.kabupaten import Kabupaten
from api.models.province import Province
from api.models.link import Link
from api.models.user import User, ApprovalRequest
from api.models.role import Role
#serializers 
from api.serializers.UserSerializers import UserSerializer
from api.serializers.PasswordChangeSerializer import PasswordChangeSerializer
from api.serializers.ProvinceSerializer import ProvinceSerializer
from api.serializers.BalaiSerializers import BalaiSerializer
from api.serializers.KabupatenSerializer import KabupatenSerializer
from api.serializers.LoginSerializer import LoginSerializer
from api.serializers.RoleSerializer import RoleSerializer
from api.serializers.LinkSerializer import LinkSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def province_dashboard(request):
    logged_in_user = request.user
    print("User Province:", logged_in_user.province)

    # Ensure the user has the required role
    if logged_in_user.role.role_name != Role.PROVINCIAL_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Fetch province links for the assigned province
        province_links = Link.objects.filter(province=logged_in_user.province)
        
        # Fetch kabupaten links that belong to kabupaten under the user's province
        kabupaten_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_users_pending_approval = User.objects.filter(
            role__role_name=Role.KABUPATEN_LG, 
            approved=False
        ) 
        approved_users = User.objects.filter(role__role_name=Role.KABUPATEN_LG, approved=True)
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)

        response_data = {
            'kabupaten_users_pending_approval': kabupaten_users_pending_approval.values(),
            "approved_users": approved_users.values(),
            "approval_requests": approval_requests.values(),
            'province_links': province_links.values(),
            'kabupaten_links': kabupaten_links.values(),  # Add kabupaten links here
        }

        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Handling approval or rejection of Balai LG users
        action = request.data.get('action')
        
        # Handling user approval/rejection
        if action in ['approve', 'reject']:
            user_id = request.data.get('user_id')
            if user_id:
                user = get_object_or_404(User, id=user_id)

                if action == 'approve':
                    user.approved = True
                    user.save()
                    return Response({'detail': f'Kabupaten LG User {user.email} has been approved.'}, status=200)
                elif action == 'reject':
                    user.approved = False
                    user.is_active = False
                    user.save()
                    return Response({'detail': f'Kabupaten LG User {user.email} has been rejected.'}, status=200)

            return Response({'detail': 'Invalid data'}, status=400)

        # Handling link creation (only for logged-in user's province)
        elif request.data.get('action') == 'create_link':
            link_serializer = LinkSerializer(data=request.data)
            if link_serializer.is_valid():
                # Ensure the link is created only for the assigned province
                province_id_from_request = request.data.get('province')
                
                if str(province_id_from_request) != str(logged_in_user.province.id):
                    return Response({"detail": "You can only create links for your assigned province."},
                                     status=status.HTTP_403_FORBIDDEN)

                # Create and save the link
                link_serializer.save()
                return Response(link_serializer.data, status=status.HTTP_201_CREATED)

            return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Update a link within the province
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, id=link_id, province=logged_in_user.province)

        link_serializer = LinkSerializer(link, data=request.data, partial=True)
        if link_serializer.is_valid():
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_200_OK)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a link within the province
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, id=link_id, province=logged_in_user.province)
        link.delete()
        return Response({'detail': 'Link deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
