from django.contrib import admin
from django.urls import path
from api.views.Api_login import api_login
from api.views.pfid_dashboard import pfid_dashboard,superadmin_dashboard
from api.views.change_password import change_password
from api.views.balai_dashboard import balai_dashboard
from api.views.province_dashboard import province_dashboard
from api.views.kabupaten_dashboard import kabupaten_dashboard
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
   
    #user login api's url 
    
    path('api/login/',api_login, name='api-login'),
    path('api/change-password/',change_password, name='change-password'),

    #hierarchy from pfid to kabupaten level 
    path('api/pfid_dashboard/',pfid_dashboard, name= "pfid_dashboard_api"),
    path('api/balai_dashboard/',balai_dashboard, name='balai_dashboard_api'),
    path('api/province/',province_dashboard, name='province_dashboard'),
    path('api/kabupaten/',kabupaten_dashboard, name='kabupaten_dashboard'),
    path('api/superadmin/',superadmin_dashboard, name='superadmin_dashboard'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
