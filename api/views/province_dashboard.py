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
from api.models.Balai import Balai
from api.models.Kabupaten import Kabupaten
from api.models.Province import Province
from api.models.Link import Link
from api.models.User import User, ApprovalRequest
from api.models.Role import Role
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

        # Fetch kabupaten links under the user's province
        kabupaten_links = Link.objects.filter(province=logged_in_user.province)

        # Get pending and approved users
        kabupaten_users_pending_approval = User.objects.filter(
            role__role_name=Role.KABUPATEN_LG, 
            approved=False
        ) 
        approved_users = User.objects.filter(role__role_name=Role.KABUPATEN_LG, approved=True)

        # Fetch approval requests assigned to the logged-in user
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)

        response_data = {
            'kabupaten_users_pending_approval': kabupaten_users_pending_approval.values(),
            'approved_users': approved_users.values(),
            'approval_requests': approval_requests.values(),
            'province_links': province_links.values(),
            'kabupaten_links': kabupaten_links.values(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        action = request.data.get('action')

        if action == 'approve' or action == 'reject':
            # Handle user approval or rejection
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

        elif action == 'register':
            # Register a new Kabupaten LG user
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            kabupaten_id = request.data.get('kabupaten')

            if not all([username, email, password, kabupaten_id]):
                return Response({'detail': 'All fields are required'}, status=400)

            if User.objects.filter(email=email).exists():
                return Response({'detail': 'User with this email already exists'}, status=400)

            kabupaten = get_object_or_404(Kabupaten, KabupatenCode=kabupaten_id)

            # Create new user
            kabupaten_user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=Role.objects.get(role_name=Role.KABUPATEN_LG),
                province=logged_in_user.province,
                Kabupaten=kabupaten,
                approved=False  # Requires approval
            )

            # Create approval request
            ApprovalRequest.objects.create(user=kabupaten_user, approver=logged_in_user, status='Pending')

            return Response({'detail': 'Registration completed. Awaiting approval.'}, status=201)

        elif action == 'create_link':
            # Create a new link for the province
            link_serializer = LinkSerializer(data=request.data)
            if link_serializer.is_valid():
                province_id_from_request = request.data.get('province')
                
                if str(province_id_from_request) != str(logged_in_user.province.provinceCode):
                    return Response({"detail": "You can only create links for your assigned province."},
                                    status=status.HTTP_403_FORBIDDEN)

                link_serializer.save()
                return Response(link_serializer.data, status=status.HTTP_201_CREATED)

            return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Invalid action provided.'}, status=400)

    elif request.method == 'PUT':
        # Update a link within the province
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, linkId=link_id, province=logged_in_user.province)

        link_serializer = LinkSerializer(link, data=request.data, partial=True)
        if link_serializer.is_valid():
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_200_OK)

        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a link within the province
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, linkId=link_id, province=logged_in_user.province)
        link.delete()
        return Response({'detail': 'Link deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)

'''@api_view(['GET', 'POST', 'PUT', 'DELETE'])
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
    elif request.method == 'POST':
        action = request.data.get('action')

        # Register a new Kabupaten LG user
        if action == 'register':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            kabupaten_id = request.data.get('kabupaten')

            # Validate required fields
            if not all([username, email, password, kabupaten_id]):
                return Response({'detail': 'All fields are required'}, status=400)

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return Response({'detail': 'User with this email already exists'}, status=400)

            # Fetch the correct Kabupaten using KabupatenCode
            kabupaten = get_object_or_404(Kabupaten, KabupatenCode=kabupaten_id)

            # Create a new Kabupaten LG user
            kabupaten_user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=Role.objects.get(role_name=Role.KABUPATEN_LG),
                province=logged_in_user.province,  # Assign same province as logged-in user
                Kabupaten=kabupaten,
                approved=False  # Requires Provincial LG approval
            )

            # Create an approval request
            ApprovalRequest.objects.create(user=kabupaten_user, approver=logged_in_user, status='Pending')

            return Response({'detail': 'Registration completed. Awaiting approval.'}, status=201)

        # Handling link creation (only for logged-in user's province)
        elif request.data.get('action') == 'create_link':
            link_serializer = LinkSerializer(data=request.data)
            if link_serializer.is_valid():
                # Ensure the link is created only for the assigned province
                province_id_from_request = request.data.get('province')
                
                if str(province_id_from_request) != str(logged_in_user.province.provinceCode):
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

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)'''
