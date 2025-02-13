from django.contrib import admin
from django.urls import path
from api.views.Api_login import api_login
from api.views.linkViews import LinkViewSet
from api.views.pfid_dashboard import pfid_dashboard,superadmin_dashboard, DPSI_dashboard, SPDJD_dashboard
from api.views.change_password import change_password
from api.views.balai_dashboard import balai_dashboard
from api.views.province_dashboard import province_dashboard
from api.views.kabupatenLink import kabupatenLink
from api.views.provinceLink import provinceLinks
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from api.views.roadInventory import roadInventory
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'link', LinkViewSet)

urlpatterns = [
   
    #user login api's url 
    path('', include(router.urls)),
    path('login',api_login, name='api-login'),
    path('change-password',change_password, name='change-password'),
    path('login',api_login, name='api-login'),
    path('change-password',change_password, name='change-password'),

    #hierarchy from pfid to kabupaten level 
    path('spdjd_dashboard',SPDJD_dashboard, name= "spdjd_dashboard_api" ),
    path('dpsi_dashboard',DPSI_dashboard, name= "dpsi_dashboard_api" ),
    path('pfid_dashboard',pfid_dashboard, name= "pfid_dashboard_api"),
    path('balai_dashboard',balai_dashboard, name='balai_dashboard_api'),
    path('province',province_dashboard, name='province_dashboard'),
    path('provinceLinks',provinceLinks, name="province_links"),
    path('kabupatenLink',kabupatenLink, name='kabupaten_links'),
    path('superadmin',superadmin_dashboard, name='superadmin_dashboard'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('road_inventory',roadInventory, name='road_inventory_list_create'),
    
]
