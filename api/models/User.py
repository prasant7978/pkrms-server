from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from api.models.Role import Role
from api.models.Balai import Balai
from api.models.Province import Province
from api.models.Kabupaten import Kabupaten


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)  # Added unique=True to username
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Full Name")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Default is False for regular users
    date_joined = models.DateTimeField(default=timezone.now)
    
    balai = models.ForeignKey(Balai, on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    Kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, null=True, blank=True)
    
    approved = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True, related_name="users")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Since email is the USERNAME_FIELD, username is required here

    def __str__(self):
        return self.username

class ApprovalRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='approval_request')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_approvals')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )