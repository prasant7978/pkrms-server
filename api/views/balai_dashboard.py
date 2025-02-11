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



@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])  
def balai_dashboard(request):
    logged_in_user = request.user

    # GET method
    if request.method == 'GET':
        province_users_pending_approval = User.objects.filter(role__role_name=Role.PROVINCIAL_LG, approved=False)
        kabupaten_users_pending_approval = User.objects.filter(role__role_name=Role.KABUPATEN_LG, approved=False)
        approved_users = User.objects.filter(role__role_name__in=[Role.PROVINCIAL_LG, Role.KABUPATEN_LG], approved=True)
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)

        return Response({
            "approved_users": list(approved_users.values()),
            "province_users_pending_approval": list(province_users_pending_approval.values()),
            "kabupaten_users_pending_approval": list(kabupaten_users_pending_approval.values()),
            "approval_requests": list(approval_requests.values()),
        })

    # POST method - Register Province LG & Kabupaten LG users
    elif request.method == 'POST':
        action = request.data.get('action')

        if action == 'register':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            balai_id = request.data.get('balai')
            province_id = request.data.get('province')
            kabupaten_id = request.data.get('kabupaten')
            role_name = request.data.get('role_name')  # Use role name instead of role ID

            # Ensure only allowed roles are used
            if role_name not in [Role.PROVINCIAL_LG, Role.KABUPATEN_LG]:
                return Response({'detail': 'Invalid role_name. Only Provincial LG and Kabupaten LG are allowed.'}, status=400)

            if not all([username, email, password, province_id, kabupaten_id, role_name]):
                return Response({'detail': 'All fields are required'}, status=400)

            if User.objects.filter(email=email).exists():
                return Response({'detail': 'User with this email already exists'}, status=400)

            balai = get_object_or_404(Balai, id=balai_id)
            province = get_object_or_404(Province, provinceCode=province_id)
            kabupaten = get_object_or_404(Kabupaten, KabupatenCode=kabupaten_id)
            role = get_object_or_404(Role, role_name=role_name)  # Fetch role by name

            # Create new user
            new_user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=role,
                balai=balai,
                province=province,
                Kabupaten=kabupaten,
                approved=False  # Requires approval
            )

            # Create approval request
            ApprovalRequest.objects.create(user=new_user, approver=logged_in_user, status='Pending')

            return Response({'detail': f'{role.role_name} registration completed. Awaiting approval.'}, status=201)

        elif action in ['approve', 'reject']:
            user_id = request.data.get('user_id')
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'User {user.email} has been approved.'}, status=200)
            elif action == 'reject':
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid action'}, status=400)

    # PUT method - Update user details
    elif request.method == 'PUT':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)

        if 'province' in request.data:
            province = get_object_or_404(Province, provinceCode=request.data.get('province'))
            user.province = province
        if 'balai' in request.data:
            balai = get_object_or_404(Balai, id=request.data.get('balai'))
            user.balai = balai
        if 'Kabupaten' in request.data:
            kabupaten = get_object_or_404(Kabupaten, KabupatenCode=request.data.get('Kabupaten'))
            user.Kabupaten = kabupaten

        user.save()
        return Response({'detail': 'User updated successfully.'}, status=200)

    # PATCH method - Partial update
    elif request.method == 'PATCH':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        if 'username' in request.data:
            user.username = request.data.get('username')
        if 'email' in request.data:
            user.email = request.data.get('email')
        if 'province' in request.data:
            user.province = get_object_or_404(Province, provinceCode=request.data.get('province'))
        if 'balai' in request.data:
            user.balai = get_object_or_404(Balai, id=request.data.get('balai'))
        if 'Kabupaten' in request.data:
            user.Kabupaten = get_object_or_404(Kabupaten, KabupatenCode=request.data.get('Kabupaten'))

        user.save()
        return Response({'detail': 'User partially updated successfully.'}, status=200)

    # DELETE method - Delete user
    elif request.method == 'DELETE':
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'User ID is required for deletion.'}, status=400)
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=204)

    return Response({'detail': 'Invalid HTTP method'}, status=405)

'''@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])  
def balai_dashboard(request):
    logged_in_user = request.user

    # GET method
    if request.method == 'GET':
        province_users_pending_approval = User.objects.filter(role__role_name=Role.PROVINCIAL_LG, approved=False)
        kabupaten_users_pending_approval = User.objects.filter(role__role_name=Role.KABUPATEN_LG, approved=False)
        approved_users = User.objects.filter(role__id__in=[5, 6], approved=True)
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)

        return Response({
            "approved_users": list(approved_users.values()),
            "province_users_pending_approval": list(province_users_pending_approval.values()),
            "kabupaten_users_pending_approval": list(kabupaten_users_pending_approval.values()),
            "approval_requests": list(approval_requests.values()),
        })

    # POST method - Register Province LG & Kabupaten LG users
    elif request.method == 'POST':
        action = request.data.get('action')

        if action == 'register':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            balai_id = request.data.get('balai')
            province_id = request.data.get('province')
            kabupaten_id = request.data.get('kabupaten')
            role_id = request.data.get('role_id')  # Role ID instead of role name

            # Ensure only allowed roles are used (5 = Province LG, 6 = Kabupaten LG)
            if role_id not in [5, 6]:
                return Response({'detail': 'Invalid role_id. Only 5 (Province LG) and 6 (Kabupaten LG) are allowed.'}, status=400)

            if not all([username, email, password, province_id, kabupaten_id, role_id]):
                return Response({'detail': 'All fields are required'}, status=400)

            if User.objects.filter(email=email).exists():
                return Response({'detail': 'User with this email already exists'}, status=400)

            balai = get_object_or_404(Balai, id=balai_id)
            province = get_object_or_404(Province, provinceCode=province_id)
            kabupaten = get_object_or_404(Kabupaten, KabupatenCode=kabupaten_id)
            role = get_object_or_404(Role, id=role_id)  # Fetch role by ID

            # Create new user
            new_user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=role,
                balai=balai,
                province=province,
                Kabupaten=kabupaten,
                approved=False  # Requires approval
            )

            # Create approval request
            ApprovalRequest.objects.create(user=new_user, approver=logged_in_user, status='Pending')

            return Response({'detail': f'{role.role_name} registration completed. Awaiting approval.'}, status=201)

        elif action in ['approve', 'reject']:
            user_id = request.data.get('user_id')
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'User {user.email} has been approved.'}, status=200)
            elif action == 'reject':
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid action'}, status=400)

    # PUT method - Update user details
    elif request.method == 'PUT':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)

        if 'province' in request.data:
            province = get_object_or_404(Province, provinceCode=request.data.get('province'))
            user.province = province
        if 'balai' in request.data:
            balai = get_object_or_404(Balai, id=request.data.get('balai'))
            user.balai = balai
        if 'Kabupaten' in request.data:
            kabupaten = get_object_or_404(Kabupaten, KabupatenCode=request.data.get('Kabupaten'))
            user.Kabupaten = kabupaten

        user.save()
        return Response({'detail': 'User updated successfully.'}, status=200)

    # PATCH method - Partial update
    elif request.method == 'PATCH':
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        if 'username' in request.data:
            user.username = request.data.get('username')
        if 'email' in request.data:
            user.email = request.data.get('email')
        if 'province' in request.data:
            user.province = get_object_or_404(Province, provinceCode=request.data.get('province'))
        if 'balai' in request.data:
            user.balai = get_object_or_404(Balai, id=request.data.get('balai'))
        if 'Kabupaten' in request.data:
            user.Kabupaten = get_object_or_404(Kabupaten, KabupatenCode=request.data.get('Kabupaten'))

        user.save()
        return Response({'detail': 'User partially updated successfully.'}, status=200)

    # DELETE method - Delete user
    elif request.method == 'DELETE':
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'User ID is required for deletion.'}, status=400)
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=204)

    return Response({'detail': 'Invalid HTTP method'}, status=405)'''







