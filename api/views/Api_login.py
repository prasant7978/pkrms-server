from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import  login
from django.http import HttpResponse
from rest_framework import serializers
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.Role import Role
from api.models.User import User,ApprovalRequest
from api.serializers.LoginSerializer import LoginSerializer
from rest_framework.permissions import BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models.Province import Province
from api.models.Kabupaten import Kabupaten
from api.models.Balai import Balai
from django.contrib.auth import get_user_model

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    API Login endpoint to authenticate a user and return a JWT token.
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        # Check if email exists in the database
        '''User = get_user_model()
        if not User.objects.filter(email=email).exists():
            return Response({'success': False, 'detail': 'Email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)'''

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Check if user is active
            if not user.is_active:
                return Response({'success': False, 'detail': 'Your account is not active.'}, status=status.HTTP_400_BAD_REQUEST)

            # Specific checks for user roles regarding approval
            role_approval_messages = {
                Role.PROVINCIAL_LG: 'Your account is pending approval from a Balai LG user.',
                Role.BALAI: 'Your account is pending approval from a higher-level admin.',
                Role.KABUPATEN_LG: 'Your account is pending approval from a Provincial LG user.',
                Role.PFID: 'Your account is pending approval from a Super Admin.',
            }

            if user.role.role_name in role_approval_messages and not user.approved:
                return Response({'success': False, 'detail': role_approval_messages[user.role.role_name]}, status=status.HTTP_400_BAD_REQUEST)

            # General approval check
            if not user.approved and not user.is_superuser:
                return Response({'success': False, 'detail': 'Your account is not approved yet. Please wait for approval.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT token for authenticated users
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Prepare response based on user role
            response_data = {
                "success": True,
                "refresh_token": str(refresh),
                "access_token": str(access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "userrole": user.role.role_name if user.role else None
                }
            }

            # Add extra fields based on the user role
            if user.role.role_name == Role.BALAI:
               response_data["user"].update({
                   "balainame": user.balai.balaiName if user.balai else None,  # Fetch only the name
                   "provincename": user.province.provinceName if user.province else None,
                   "approved": user.approved
                })


            elif user.role.role_name == Role.PROVINCIAL_LG:
                 response_data["user"].update({
                    "balainame": user.balai.balaiName if user.balai else None,
                    "provincename": user.province.provinceName if user.province else None,
                    "approved": user.approved,
                    "kabupaten_name": user.Kabupaten.KabupatenName  if user.Kabupaten else None
               })

            elif user.role.role_name == Role.KABUPATEN_LG:
                response_data["user"].update({
                   "balainame": user.balai.balaiName if user.balai else None,  # Corrected field
                   "approved": user.approved,
                   "kabupaten_name": user.Kabupaten.KabupatenName  if user.Kabupaten else None
                })

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'success': False, 'detail': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
