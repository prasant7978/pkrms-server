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


from rest_framework.permissions import BasePermission
from django.contrib.auth.hashers import make_password






# API for balai_dashboard
@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])  
def balai_dashboard(request):
    logged_in_user = request.user

    # GET method
    if request.method == 'GET':
        # Fetching users and approval requests
        province_users_pending_approval = User.objects.filter(
            role__role_name=Role.PROVINCIAL_LG, 
            approved=False
        )
        approved_users = User.objects.filter(role__role_name=Role.PROVINCIAL_LG, approved=True)
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)

        # Fetching links for province and kabupaten
        province_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)

        return Response({
            "approved_users": list(approved_users.values()),
            "province_users_pending_approval": list(province_users_pending_approval.values()),
            "approval_requests": list(approval_requests.values()),
            'province_links': list(province_links.values()),
            'kabupaten_links': list(kabupaten_links.values())
        })

    # POST method - Handle registration and approval/rejection actions
    elif request.method == 'POST':
        action = request.data.get('action')

        # Registration for Province LG user
        if action == 'register':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            balai_id = request.data.get('balai')
            province_id = request.data.get('province')
            kabupaten_id = request.data.get('Kabupaten')

            # Validate required fields
            if not all([username, email, password, province_id, kabupaten_id]):
                return Response({'detail': 'All fields are required'}, status=400)

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return Response({'detail': 'User with this email already exists'}, status=400)

            # Fetch province and kabupaten objects
            balai = get_object_or_404(Balai, id=balai_id)
            province = get_object_or_404(Province, id=province_id)
            kabupaten = get_object_or_404(Kabupaten, id=kabupaten_id)

            # Create new user with the role of Provincial LG
            province_user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=Role.objects.get(role_name=Role.PROVINCIAL_LG),
                balai=balai,
                province=province,
                Kabupaten=kabupaten,
                approved=False  # Requires Balai LG approval
            )

            # Create approval request for the new user
            ApprovalRequest.objects.create(user=province_user, approver=logged_in_user, status='Pending')

            return Response({'detail': 'Registration completed. Awaiting Balai LG approval.'}, status=201)

        # Approval or rejection of Provincial LG users
        elif action in ['approve', 'reject']:
            user_id = request.data.get('user_id')
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'Province LG User {user.email} has been approved.'}, status=200)
            elif action == 'reject':
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'Province LG User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid action'}, status=400)

    # PUT method - Update user details
    elif request.method == 'PUT':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        # You can update user attributes here based on the request data
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        
        if 'province' in request.data:
            province_id = request.data.get('province')
            province = get_object_or_404(Province, id=province_id)
            user.province = province
        if 'balai' in request.data:
            balai_id = request.data.get('balai')
            balai = get_object_or_404(Balai, id=balai_id)
            user.balai = balai
        if 'Kabupaten' in request.data:
            kabupaten_id = request.data.get('Kabupaten')
            kabupaten = get_object_or_404(Kabupaten, id=kabupaten_id)
            user.Kabupaten = kabupaten

        user.save()
        return Response({'detail': 'User updated successfully.'}, status=200)
     # PATCH method: Partial update of Provincial LG user details (password not updated)
    elif request.method == 'PATCH':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        # Update only the fields provided in the request
        if 'username' in request.data:
            user.username = request.data.get('username', user.username)
        if 'email' in request.data:
            user.email = request.data.get('email', user.email)
        if 'province' in request.data:
            province_id = request.data.get('province')
            province = get_object_or_404(Province, id=province_id)
            user.province = province
        if 'balai' in request.data:
            balai_id = request.data.get('balai')
            balai = get_object_or_404(Balai, id=balai_id)
            user.balai = balai
        if 'Kabupaten' in request.data:
            kabupaten_id = request.data.get('Kabupaten')
            kabupaten = get_object_or_404(Kabupaten, id=kabupaten_id)
            user.Kabupaten = kabupaten

        user.save()
        return Response({'detail': 'User partially updated successfully.'}, status=200)

    # DELETE method: Delete a Provincial LG user
    elif request.method == 'DELETE':
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'User ID is required for deletion.'}, status=400)
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=204)

    return Response({'detail': 'Invalid HTTP method'}, status=405)
    