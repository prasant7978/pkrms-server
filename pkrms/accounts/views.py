from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Traffic_weighting_factors
from .models import ApprovalRequest, Traffic_volume,Traffic_weighting_factors,Link,Retaining_walls,Retaining_walls_Condition,CulvertCondition,CulvertInventory,RoadCondition, DRP,RoadInventory, Province, Kabupaten , LinkClass,  PriorityArea,LinkKabupaten, LinkKacematan
from rest_framework import serializers
from .serializers import RoadInventorySerializer, RoadInventorySerializer, LinkSerializer, DRPSerializer , LinkClassSerializer, LinkKabupatenSerializer, LinkKacematanSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from django.shortcuts import render, redirect
from .serializers import  RoadConditionSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.http import HttpResponse

from rest_framework.permissions import AllowAny
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, OTPVerificationSerializer
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Role, Balai, Province, Kabupaten
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Retaining_walls_Condition, Link, ApprovalRequest, Retaining_walls
from .serializers import RetainingWallsConditionSerializer, ApprovalRequestSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.hashers import check_password

from rest_framework import viewsets
from .models import Balai, Province, Kabupaten
from .serializers import BalaiSerializer, ProvinceSerializer, KabupatenSerializer
# registration modules 
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from rest_framework.permissions import BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, ApprovalRequest, Link, Role
from .serializers import UserSerializer, ApprovalRequestSerializer
from django.shortcuts import get_object_or_404



class BalaiViewSet(viewsets.ModelViewSet):
    queryset = Balai.objects.all()
    serializer_class = BalaiSerializer

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class KabupatenViewSet(viewsets.ModelViewSet):
    queryset = Kabupaten.objects.all()
    serializer_class = KabupatenSerializer
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registers a user and sends OTP to the user's email.
    """
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            role_id = serializer.validated_data['role']
            balai_id = serializer.validated_data.get('balai')
            province_id = serializer.validated_data.get('province')
            kabupaten_id = serializer.validated_data.get('kabupaten')
            password = serializer.validated_data['password']

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(email=email).exists():
                return Response({'detail': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate Role, Balai, Province, and Kabupaten
            try:
                role = Role.objects.get(id=role_id)
                balai = Balai.objects.get(id=balai_id) if balai_id else None
                province = Province.objects.get(id=province_id) if province_id else None
                kabupaten = Kabupaten.objects.get(id=kabupaten_id) if kabupaten_id else None
            except (Role.DoesNotExist, Balai.DoesNotExist, Province.DoesNotExist, Kabupaten.DoesNotExist):
                return Response({'detail': 'Invalid role or location data.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if OTP is already sent to this email
            cached_otp = cache.get(email)
            if cached_otp:
                return Response({'detail': 'OTP already sent. Please verify it.'}, status=status.HTTP_400_BAD_REQUEST)
            # Generate OTP and cache it for 5 minutes
            otp = random.randint(1000, 9999)
            cache.set(email, otp, timeout=300)

            # Send OTP email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Store user data in session (we will store it in the request data for simplicity in the API)
            request.session['user_data'] = {
                'username': username,
                'email': email,
                'role': role.id,
                'balai': balai.id if balai else None,
                'province': province.id if province else None,
                'kabupaten': kabupaten.id if kabupaten else None,
                'password': password,
            }

            return Response({'detail': 'OTP sent successfully. Please verify it.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verifies OTP and completes user registration if OTP is correct.
    """
    if request.method == 'POST':
        serializer = OTPVerificationSerializer(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            user_data = request.session.get('user_data')

            if not user_data:
                return Response({'detail': 'Session expired. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)

            cached_otp = cache.get(user_data['email'])

            if str(otp) == str(cached_otp):
                # Create the user
                user = User.objects.create_user(
                    email=user_data['email'],
                    username=user_data['username'],
                    password=user_data['password'],
                    role_id=user_data['role'],
                    balai_id=user_data.get('balai'),
                    province_id=user_data.get('province'),
                    Kabupaten_id=user_data.get('kabupaten'),
                    approved=(user_data['role'] == 'balai_lg'),  # Auto-approve Balai LG users
                )

                # Clear session and cache
                cache.delete(user_data['email'])
                del request.session['user_data']

                return Response({'detail': 'Registration successful.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        user = authenticate(request, email=email, password=password)

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
            
            elif user.role.role_name == Role.BALAI_LG:
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
                'user_id': user.id,
                'email': user.email,
                'role': user.role.role_name if user.role else None,
                'message': f'User {user.email} logged in successfully.'
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

#API for PFID dashboard 
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pfid_dashboard(request):
    logged_in_user = request.user

    if request.method == 'GET':
        # Fetching users pending approval for BALAI_LG role
        balai_users_pending_approval = User.objects.filter(
            role__role_name=Role.BALAI_LG,
            approved=False
        )

        # Fetching approved Balai LG users
        approved_balai_users = User.objects.filter(role__role_name=Role.BALAI_LG, approved=True)
        print(f"Approved Balai LG users count: {approved_balai_users.count()}")  # Debug

        # Fetching all approval requests for the logged-in PFID user
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)
        print(f"Pending approval requests count: {approval_requests.count()}")  # Debug

        # Fetching province and kabupaten links
        province_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
        retaining_wall_province = Retaining_walls.objects.filter(province=logged_in_user.province)
        #retaining_wall_kabupaten = Retaining_walls.objects.filter(kabupaten=logged_in_user.kabupaten)
        links= Link.objects.all()
        # Serializing the data
        user_serializer = UserSerializer(balai_users_pending_approval, many=True)
        approved_user_serializer = UserSerializer(approved_balai_users, many=True)
        approval_request_serializer = ApprovalRequestSerializer(approval_requests, many=True)

        # Adding the province and kabupaten links to the response data
        return Response({
            'balai_users_pending_approval': user_serializer.data,
            'approved_balai_users': approved_user_serializer.data,
            'approval_requests': approval_request_serializer.data,
            'province_links': list(province_links.values()),
            'kabupaten_links': list(kabupaten_links.values()),
            'links': list(links.values()),
            #"retaining_wall_kabupaten": list(retaining_wall_kabupaten.values()),
            "retaining_wall_province": list(retaining_wall_province.values())
        })

    elif request.method == 'POST':
        # Handling approval or rejection of Balai LG users
        user_id = request.data.get('user_id')
        action = request.data.get('action')

        if user_id:
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'Balai LG User {user.email} has been approved.'}, status=200)
            elif action == 'reject':
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'Balai LG User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid data'}, status=400)


# API for balai_dashboard
@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def balai_dashboard(request):
    logged_in_user = request.user

    if request.method == 'GET':
        # Existing code for fetching users and links
        province_users_pending_approval = User.objects.filter(
            role__role_name=Role.PROVINCIAL_LG, 
            approved=False
        )
        approved_users = User.objects.filter(role__role_name=Role.PROVINCIAL_LG, approved=True)
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)

       # Fetching province and kabupaten links
        province_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.kabupaten)
        #retaining_wall_province = Retaining_walls.objects.filter(province=logged_in_user.province)
        #retaining_wall_kabupaten = Retaining_walls.objects.filter(Kabupaten=logged_in_user.kabupaten)
        #links= Link.objects.all()
        #
        # Adding the province and kabupaten links to the response data
        return Response({
            "approved_users":list(approved_users.values()),
            "province_users_pending_approval": list(province_users_pending_approval.values()),
            "approval_requests":list(approval_requests.values()),
            'province_links': list(province_links.values()),
            'kabupaten_links': list(kabupaten_links.values()),
            #'links': list(links.values()),
            #"retaining_wall_kabupaten": list(retaining_wall_kabupaten.values()),
            #"retaining_wall_province": list(retaining_wall_province.values())
        })

    elif request.method == 'POST':
        # Handling approval or rejection of Balai LG users
        user_id = request.data.get('user_id')
        action = request.data.get('action')

        if user_id:
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'province LG User {user.email} has been approved.'}, status=200)
            elif action == 'reject':
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'province LG User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid data'}, status=400)
    
    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def province_dashboard(request):
    logged_in_user = request.user

    # Ensure the user has the required role
    if logged_in_user.role.role_name != Role.PROVINCIAL_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Fetch province and kabupaten links for the assigned province
        province_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_links = Link.objects.filter(kabupaten__province=logged_in_user.province)

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
            'kabupaten_links': kabupaten_links.values()
        }

        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Handling approval or rejection of Balai LG users
        user_id = request.data.get('user_id')
        action = request.data.get('action')

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

    elif request.method == 'POST' and request.data.get('action') == 'create_link':
        # Logic to create a link for the assigned province
        link_serializer = LinkSerializer(data=request.data)
        if link_serializer.is_valid():
            # Ensure the link is created only for the assigned province
            if str(request.data.get('province')) != str(logged_in_user.province.id):
                return Response({"detail": "You can only create links for your assigned province."},
                                 status=status.HTTP_403_FORBIDDEN)

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

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def kabupaten_dashboard(request):
    logged_in_user = request.user

    # Ensure the user has the required role
    if logged_in_user.role.role_name != Role.KABUPATEN_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Fetch links associated with the logged-in user's kabupaten
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.kabupaten)

        # Serialize data
        response_data = {
            'kabupaten_links': kabupaten_links.values(),
        }
        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        action = request.data.get('action')

        if action == 'create_link':
            link_serializer = LinkSerializer(data=request.data)
            if link_serializer.is_valid():
                if request.data.get('kabupaten') != str(logged_in_user.kabupaten.id):
                    return Response({"detail": "You can only create links for your assigned kabupaten."},
                                    status=status.HTTP_403_FORBIDDEN)
                link_serializer.save()
                return Response(link_serializer.data, status=status.HTTP_201_CREATED)
            return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, id=link_id, kabupaten=logged_in_user.kabupaten)
        
        link_serializer = LinkSerializer(link, data=request.data, partial=True)
        if link_serializer.is_valid():
            link_serializer.save()
            return Response(link_serializer.data, status=status.HTTP_200_OK)
        return Response(link_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        link_id = request.data.get('link_id')
        link = get_object_or_404(Link, id=link_id, kabupaten=logged_in_user.kabupaten)
        link.delete()
        return Response({'detail': 'Link deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'detail': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)





