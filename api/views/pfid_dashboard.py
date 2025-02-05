from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import random
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from api.models.province import Province
from api.models.balai import Balai
from api.models.kabupaten import Kabupaten
from api.models.link import Link
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from api.models.user import User, ApprovalRequest
from api.models.role import Role
from api.serializers.UserSerializers import UserSerializer
from api.serializers.UserSerializers import ApprovalRequestSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
#api for superadmin

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def superadmin_dashboard(request):
    """
    View for Super Admin to approve or reject PFID users.
    """
    logged_in_user = request.user

    # Ensure only superadmin can access this view
    if not logged_in_user.is_superuser:
        return Response({'detail': 'You do not have permission to access this view.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Fetching PFID users pending approval
        pfid_users_pending_approval = User.objects.filter(
            role__role_name=Role.PFID,
            approved=False
        )

        # Fetching approved PFID users
        approved_pfid_users = User.objects.filter(role__role_name=Role.PFID, approved=True)
        print(f"Approved PFID users count: {approved_pfid_users.count()}")  # Debug

        # Fetching all approval requests assigned to the superadmin
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)
        print(f"Pending approval requests count: {approval_requests.count()}")  # Debug

        

        # Serializing the data
        user_serializer = UserSerializer(pfid_users_pending_approval, many=True)
        approved_user_serializer = UserSerializer(approved_pfid_users, many=True)
        approval_request_serializer = ApprovalRequestSerializer(approval_requests, many=True)

        # Adding all links to the response data
        return Response({
            'pfid_users_pending_approval': user_serializer.data,
            'approved_pfid_users': approved_user_serializer.data,
            'approval_requests': approval_request_serializer.data,
            
        })

    elif request.method == 'POST':
        # Handling approval or rejection of PFID users
        user_id = request.data.get('user_id')
        action = request.data.get('action')

        if user_id:
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'PFID User {user.email} has been approved.'}, status=200)
            elif action == 'reject':
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'PFID User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid data'}, status=400)

#pfid dashboard


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def pfid_dashboard(request):
    logged_in_user = request.user

    # GET method - Fetches data
    if request.method == 'GET':
        balai_users_pending_approval = User.objects.filter(role__role_name=Role.BALAI_LG, approved=False)
        approved_balai_users = User.objects.filter(role__role_name=Role.BALAI_LG, approved=True)
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)

        province_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
        #retaining_wall_province = Retaining_walls.objects.filter(province=logged_in_user.province)
        links = Link.objects.all()

        user_serializer = UserSerializer(balai_users_pending_approval, many=True)
        approved_user_serializer = UserSerializer(approved_balai_users, many=True)
        approval_request_serializer = ApprovalRequestSerializer(approval_requests, many=True)

        return Response({
            'balai_users_pending_approval': user_serializer.data,
            'approved_balai_users': approved_user_serializer.data,
            'approval_requests': approval_request_serializer.data,
            'province_links': list(province_links.values()),
            'kabupaten_links': list(kabupaten_links.values()),
            'links': list(links.values()),
            #'retaining_wall_province': list(retaining_wall_province.values())
        })

    # POST method - Handles user registration and approvals
    elif request.method == 'POST':
        action = request.data.get('action')

        if action == 'register':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            balai_id = request.data.get('balai')
            province_id = request.data.get('province')
            kabupaten_id = request.data.get('Kabupaten')

            # Validate required fields
            if not all([username, email, password, balai_id, province_id, kabupaten_id]):
                return Response({'detail': 'All fields are required'}, status=400)

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return Response({'detail': 'User with this email already exists'}, status=400)

            # Fetch province, kabupaten, and balai objects
            balai = get_object_or_404(Balai, id=balai_id)
            province = get_object_or_404(Province, id=province_id)
            kabupaten = get_object_or_404(Kabupaten, id=kabupaten_id)

            # Create new user
            balai_user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=Role.objects.get(role_name=Role.BALAI_LG),
                balai=balai,
                province=province,
                Kabupaten=kabupaten,
                approved=False  # Requires PFID approval
            )

            # Create approval request
            ApprovalRequest.objects.create(user=balai_user, approver=logged_in_user, status='Pending')

            return Response({'detail': 'Registration completed. Awaiting PFID approval.'}, status=201)

        elif action in ['approve', 'reject']:
            user_id = request.data.get('user_id')
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'Balai LG User {user.email} has been approved.'}, status=200)
            else:
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'Balai LG User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid action'}, status=400)

    # PUT method - Update user details
    elif request.method == 'PUT':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        # You can update user attributes here based on the request data
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        # Update province if provided
        # Update province if provided
        if 'province' in request.data:
            province_id = request.data.get('province')
            province = get_object_or_404(Province, id=province_id)
            user.province = province

        if 'balai' in request.data:
            balai_id = request.data.get('balai')
            balai = get_object_or_404(Balai, id=balai_id)
            user.balai = balai
        user.province = get_object_or_404(Province, id=request.data.get('province', user.province.id))
        user.Kabupaten = get_object_or_404(Kabupaten, id=request.data.get('Kabupaten', user.Kabupaten.id))

        user.save()
        return Response({'detail': 'User updated successfully.'}, status=200)

    # PATCH method - Partially update user details
    elif request.method == 'PATCH':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        # Update only the fields that are provided in the request
        if 'username' in request.data:
            user.username = request.data['username']
        if 'email' in request.data:
            user.email = request.data['email']

        if 'balai' in request.data:
            balai_id = request.data['balai']
            balai = get_object_or_404(Balai, id=balai_id)
            user.balai = balai
        if 'province' in request.data:
            user.province = get_object_or_404(Province, id=request.data['province'])
        if 'Kabupaten' in request.data:
            user.Kabupaten = get_object_or_404(Kabupaten, id=request.data['Kabupaten'])

        user.save()
        return Response({'detail': 'User updated successfully.'}, status=200)

    # DELETE method - Delete user
    elif request.method == 'DELETE':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        # Soft delete by setting is_active to False
        user.is_active = False
        user.save()

        return Response({'detail': f'User {user.email} has been deleted.'}, status=200)

    return Response({'detail': 'Invalid HTTP method'}, status=405)