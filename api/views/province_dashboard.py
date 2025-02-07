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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def province_dashboard(request):
    logged_in_user = request.user
    
    # Ensure the user has the required role
    if logged_in_user.role.role_name != Role.PROVINCIAL_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)
    
    return Response({'detail': 'Invalid action provided.'}, status=400)