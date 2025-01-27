from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import BalaiViewSet, ProvinceViewSet, KabupatenViewSet, balai_dashboard,RoadInventoryAPIView
from .views import Traffic_weighting_factors
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
# Define the Swagger schema view

urlpatterns = [
   
    
    # OTP REGISTRATION on user email     
    
    path('api/register/', views.register_user, name='register_user'),
    path('api/verify-otp/', views.verify_otp, name='verify_otp'),
    path('api/login/', views.api_login, name='api-login'),
    #hierarchy from pfid to kabupaten level 
    path('api/pfid_dashboard/',views.pfid_dashboard, name= "pfid_dashboard_api"),
    path('api/balai_dashboard/', views.balai_dashboard, name='balai_dashboard_api'),
    path('api/province/', views.province_dashboard, name='province_dashboard'),
    path('api/kabupaten/', views.kabupaten_dashboard, name='kabupaten_dashboard'),
    path('api/superadmin/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('road-inventory/', RoadInventoryAPIView.as_view(), name='road_inventory_list_create'),

    # For retrieving, updating, partially updating, and deleting a specific RoadInventory
    path('road-inventory/<int:pk>/', RoadInventoryAPIView.as_view(), name='road_inventory_detail')
]


