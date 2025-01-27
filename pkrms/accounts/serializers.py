from rest_framework import serializers
from .models import Link,User,Role, DRP, LinkClass , RoadInventory, ConditionYear, RoadCondition , MCAcriteria

class LinkSerializer(serializers.ModelSerializer):
    province_code = serializers.CharField(source="province.code", read_only=True)
    kabupaten_code = serializers.CharField(source="kabupaten.code", read_only=True)

    class Meta:
        model = Link
        fields = [
            "id",
            "link_status",
            "link_number",
            "link_name",
            "link_function",
            "official_length_km",
            "actual_length_km",
            "highest_access",
            "province_code",
            "kabupaten_code",
        ]

class DRPSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRP
        fields = ['id', 'drp_number', 'chainage', 'drp_length', 'drp_type', 'drp_description', 'comment',
                  'gps_north_degree', 'gps_north_minute', 'gps_north_second',
                  'gps_east_degree', 'gps_east_minute', 'gps_east_second']


class LinkClassSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)
    kabupaten_name = serializers.CharField(source='kabupaten.name', read_only=True)
    link_name = serializers.CharField(source='link.link_name', read_only=True)
    
    # Explicit fields
    total_length = serializers.IntegerField()
    unit = serializers.CharField()
    
    class Meta:
        model = LinkClass
        fields = [
            'id',
            'province',
            'province_name',
            'kabupaten',
            'kabupaten_name',
            'link',
            'link_name',
            'total_length',
            'unit',
            'link_class',
        ]
from .models import LinkKabupaten, LinkKacematan

class LinkKabupatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkKabupaten
        fields = '__all__'


class LinkKacematanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkKacematan
        fields = '__all__'
   
class RoadInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadInventory
        fields = '__all__'
class ConditionYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionYear
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RoadConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadCondition
        fields = '__all__'


class MCAcriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCAcriteria
        fields = [
            'id',
            'link',
            'kabupaten',
            'province',
            'link_status',
            'link_number',
            'MCA_1',
            'MCA_2',
            'MCA_3',
            'MCA_4'
        ]
        read_only_fields = ['link_number']



from .models import Balai, Province, Kabupaten

class BalaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balai
        fields = ['id', 'name', 'balai_code']

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'balai', 'code', 'name', 'default_province', 'stable_network_objective']

class KabupatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kabupaten
        fields = ['id', 'province', 'balai', 'name', 'code', 'default_kabupaten', 'stable_network_objective']





from .models import User, Role, Balai, Province, Kabupaten

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(max_length=50)
    balai = serializers.CharField(required=False)
    province = serializers.IntegerField(required=False)
    kabupaten = serializers.IntegerField(required=False)

class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    province = serializers.StringRelatedField()  # If you want just the name, use `StringRelatedField()`
    Kabupaten = serializers.StringRelatedField()
    balai = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name', 'is_active', 'is_staff', 'date_joined', 'approved', 'role', 'province', 'Kabupaten', 'balai']

from .models import Role, User, ApprovalRequest

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_name']
class ApprovalRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    approver = UserSerializer(read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = ['user', 'approver', 'created_at', 'status']



from rest_framework import serializers
from .models import Retaining_walls_Condition

class RetainingWallsConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retaining_walls_Condition
        fields = '__all__'
        
from .models  import RoadInventory
class RoadInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadInventory
        fields = "__all__"



















'''from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Role, Balai, Province, Kabupaten
import random

def registrationview(request):
    balai = Balai.objects.all()
    province = Province.objects.all()
    kabupaten = Kabupaten.objects.all()
    role = Role.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        role_id = request.POST['role']  # Role ID from the form
        balai_id = request.POST.get('balai')  # Balai ID from the form
        province_id = request.POST.get('province')  # Province ID from the form
        kabupaten_id = request.POST.get('kabupaten')  # Kabupaten ID from the form
        
        password = request.POST['password']

        # Check if the username or email already exists in the User model
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')
        else:
            # Validate Role, Balai, Province, and Kabupaten before storing the OTP
            try:
                role = Role.objects.get(id=role_id)
                balai = Balai.objects.get(id=balai_id) if balai_id else None
                province = Province.objects.get(id=province_id) if province_id else None
                kabupaten = Kabupaten.objects.get(id=kabupaten_id) if kabupaten_id else None
            except (Role.DoesNotExist, Balai.DoesNotExist, Province.DoesNotExist, Kabupaten.DoesNotExist):
                messages.error(request, 'Invalid role or location data.')
                return redirect('register')

            # Generate OTP and cache it
            otp = random.randint(1000, 9999)
            cache.set(email, otp, timeout=300)  # Cache the OTP for 5 minutes
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Store user data in session
            request.session['user_data'] = {
                'username': username,
                'email': email,
                'role': role.id,  # Storing role ID
                'balai': balai.id if balai else None,
                'province': province.id if province else None,
                'kabupaten': kabupaten.id if kabupaten else None,
                
                'password': password,
            }
            return redirect('verify_otp')
        
    context = {
        'balai': balai,
        'province': province,
        'kabupaten': kabupaten,
        'role': role,
    }
    return render(request, 'register.html', context )


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from .models import User, Role, Balai, Province, Kabupaten


    
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        user_data = request.session.get('user_data')

        if not user_data:
            messages.error(request, 'Session expired. Please register again.')
            return redirect('register')

        cached_otp = cache.get(user_data['email'])
        if str(otp) == str(cached_otp):
            approver = None
            if user_data['role'] == 'province_lg' and user_data.get('balai'):
                approver = User.objects.filter(balai_id=user_data['balai'], role__name='balai_lg').first()
            elif user_data['role'] == 'kabupaten_lg' and user_data.get('province'):
                approver = User.objects.filter(province_id=user_data['province'], role__name='province_lg').first()

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

            if approver:
                ApprovalRequest.objects.create(user=user, approver=approver)

            # Clear session and cache
            cache.delete(user_data['email'])
            del request.session['user_data']

            messages.success(
                request,
                'Registration successful. Awaiting approval.' if approver else 'Account registered successfully.'
            )
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active and (user.approved or user.is_superuser):
                auth_login(request, user)
                print(f"User {user.email} logged in successfully.")
                print(f"User is_authenticated: {request.user.is_authenticated}")
                print(f"User role: {user.role}")
                if user.role:
                    role_name = user.role.role_name
                    print(f"Role name: {role_name}")

                    # Role-based redirection
                    if role_name == Role.BALAI_LG:
                        return redirect('balai_dashboard')
                    elif role_name == Role.PROVINCIAL_LG:
                        return redirect('province_dashboard')
                    elif role_name == Role.KABUPATEN_LG:
                        return redirect('kabupaten_dashboard')
                    else:
                        messages.error(request, 'Invalid role assigned.')
                        return redirect('login')
                else:
                    messages.error(request, 'User does not have an assigned role.')
                    return redirect('login')
            else:
                if not user.is_active:
                    messages.error(request, 'Your account is not active.')
                else:
                    messages.error(request, 'Your account is not approved yet. Please wait for approval.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')




from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


@login_required
def approve_request(request, request_id):
    # Get the approval request that the Balai LG needs to approve/reject
    approval_request = get_object_or_404(ApprovalRequest, id=request_id, approver=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            approval_request.status = 'Approved'
            approval_request.user.approved = True  # Set user as approved
            approval_request.user.save()  # Save user to apply approval
        elif action == 'reject':
            approval_request.status = 'Rejected'
        approval_request.save()  # Save the approval request status

        messages.success(request, f"Request has been {approval_request.status.lower()}.")
        return redirect('balai_dashboard')  # Redirect to the balai dashboard
    
    # If not a POST request, render the approval request page
    return render(request, 'approve_request.html', {'approval_request': approval_request})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Role

@login_required
def balai_dashboard(request):
    logged_in_user = request.user
    # Fetch the users who are awaiting approval for Balai LG
    province_users_pending_approval = User.objects.filter(
        role__role_name=Role.PROVINCIAL_LG, 
        approved=False
    )
    province_links = Link.objects.filter(province=logged_in_user.province)
    kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
    if request.method == 'POST':
        # Get the user_id and action (approve or reject) from the POST request
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        if user_id:
            user = get_object_or_404(User, id=user_id)
            
            if action == 'approve':
                # Mark user as approved
                user.approved = True
                user.save()
                messages.success(request, f"User {user.email} has been approved.")
            
            elif action == 'reject':
                # Mark user as rejected
                user.approved = False  # You can also create a 'rejected' field if needed
                user.is_active = False  # Disable the user from logging in
                user.save()
                messages.warning(request, f"User {user.email} has been rejected and will not be able to log in.")

        # Redirect back to the dashboard to reflect changes
        return redirect('balai_dashboard')

    # Pass the pending approval users to the template
    return render(request, 'balai_dashboard.html', {
        'province_users_pending_approval': province_users_pending_approval, 'province_links' : province_links ,
        'kabupaten_links' : kabupaten_links
    })


    

@login_required
def province_dashboard(request):
    logged_in_user = request.user
    if request.user.role.role_name != Role.PROVINCIAL_LG:
        messages.error(request, "Unauthorized access.")
          # Redirect to a default dashboard
    province_links = Link.objects.filter(province=logged_in_user.province)
    kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
    # Get pending approval requests for Kabupaten users
    kabupaten_users_pending_approval = ApprovalRequest.objects.filter(
        user__role__role_name=Role.KABUPATEN_LG, 
        status='Pending',
        approver=request.user
    )

    if request.method == 'POST':
        # Handle approval or rejection
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if request_id:
            approval_request = get_object_or_404(ApprovalRequest, id=request_id, approver=request.user)

            if action == 'approve':
                approval_request.status = 'Approved'
                approval_request.user.approved = True
                approval_request.user.save()
                approval_request.save()
                messages.success(request, f"User {approval_request.user.email} has been approved.")

            elif action == 'reject':
                approval_request.status = 'Rejected'
                approval_request.user.is_active = False
                approval_request.user.save()
                approval_request.save()
                messages.warning(request, f"User {approval_request.user.email} has been rejected.")

            return redirect('province_dashboard')  # Redirect to refresh the list

    return render(request, 'province_dashboard.html', {
        'kabupaten_users_pending_approval': kabupaten_users_pending_approval, 'province_links':province_links , 
        'kabupaten_links': kabupaten_links
    })


@login_required
def kabupaten_dashboard(request):
    logged_in_user = request.user

    # Ensure the user has the appropriate role
    if logged_in_user.role.role_name != Role.KABUPATEN_LG:
        messages.error(request, "Unauthorized access.")
        return redirect('default_dashboard')  # Redirect to a default dashboard or error page

    # Filter links belonging to the user's kabupaten
    kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)

    # Fetch pending approval requests for users under this kabupaten
    if request.method == 'POST':
        # Handle approval or rejection of user requests
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if request_id:
            approval_request = get_object_or_404(ApprovalRequest, id=request_id, approver=request.user)

            if action == 'approve':
                approval_request.status = 'Approved'
                approval_request.user.approved = True
                approval_request.user.save()
                approval_request.save()
                messages.success(request, f"User {approval_request.user.email} has been approved.")

            elif action == 'reject':
                approval_request.status = 'Rejected'
                approval_request.user.is_active = False
                approval_request.user.save()
                approval_request.save()
                messages.warning(request, f"User {approval_request.user.email} has been rejected.")

            return redirect('kabupaten_dashboard')  # Redirect to refresh the list

    # Prepare the context for rendering the dashboard
    context = {
        'kabupaten_links': kabupaten_links,
    }

    return render(request, 'kabupaten_dashboard.html', context)








def super_admin_dashboard(request):
    user = User.objects.get(id=request.session['user_id'])

    # Super Admin should have access to all data (Provinces, Balai, Kabupaten)
    if user.user_level == 'super_admin':
        provinces = Province.objects.all()
        balais = balais.objects.all()
        kabupatens = Kabupaten.objects.all()
        context = {
            'user': user,
            'provinces': provinces,
            'balais': balais,
            'kabupatens': kabupatens,
        }
        return render(request, 'super_admin_dashboard.html', context)
    else:
        return HttpResponse("You are not authorized to view this page.")'''
