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
from Crypto.Cipher import AES
import base64

from api.views.decryption import decrypt_password

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    API Login endpoint to authenticate a user and return a JWT token.
    """
    serializer = LoginSerializer(data=request.data)
    print("req: ", request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        encrypted_password = serializer.validated_data['password']

        # try:
            # Decrypt the password
        #     decrypted_password = decrypt_password(encrypted_password)
        # except ValueError:
        #     return Response({'detail': 'Invalid password encryption.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user with decrypted password
        user = authenticate(request, email=email, password=encrypted_password)

        if user is not None:
            # Check if user is active
            if not user.is_active:
                return Response({'detail': 'Your account is not active.'}, status=status.HTTP_400_BAD_REQUEST)

            # Specific checks for user roles
            if user.role.role_name == Role.PROVINCIAL_LG:
                if not user.approved:
                    return Response({
                        'detail': 'Your account is pending approval from a Balai LG user.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            elif user.role.role_name == Role.BALAI:
                if not user.approved:
                    return Response({
                        'detail': 'Your account is pending approval from a higher-level admin.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif user.role.role_name == Role.KABUPATEN_LG:
                if not user.approved:
                    return Response({
                        'detail': 'Your account is pending approval from a Provincial LG user.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            elif user.role.role_name == Role.PFID:
                if not user.approved:
                    return Response({
                        'detail': 'Your account is pending approval from a Super Admin.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # General approval check
            if not user.approved and not user.is_superuser:
                return Response({'detail': 'Your account is not approved yet. Please wait for approval.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT token for authenticated users
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response_data = {
                'refresh_token': str(refresh),
                'access_token': str(access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role.role_name if user.role else None,
                    'contact_person': user.contact_person,  # Assuming this field exists
                    'phone_number': user.phoneNumber,  # Assuming this field exists
                },
                'message': f'User {user.email} logged in successfully.'
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
