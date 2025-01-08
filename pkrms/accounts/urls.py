from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import BalaiViewSet, ProvinceViewSet, KabupatenViewSet, balai_dashboard
from .views import Traffic_weighting_factors, MCAcriteriaListCreateView, MCAcriteriaRetrieveUpdateDestroyView,ConditionYearListCreateView,ConditionYearRetrieveUpdateDeleteView,RoadConditionListCreateView,RoadConditionRetrieveUpdateDeleteView, RoadInventoryListCreateView, RoadInventoryDetailView ,LinkClassListView, link_selection_view , LinkKabupatenListCreateView,LinkKabupatenDetailView,LinkKacematanListCreateView,LinkKacematanDetailView
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

# Define the Swagger schema view

urlpatterns = [
   
    path('api/link-selection/', link_selection_view, name='link_selection'),
    


    # Balai URLs
    path('api/balais/', BalaiViewSet.as_view({'get': 'list', 'post': 'create'}), name='balai-list'),
    path('api/balais/<int:pk>/', BalaiViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='balai-detail'),

    # Province URLs
    path('api/provinces/', ProvinceViewSet.as_view({'get': 'list', 'post': 'create'}), name='province-list'),
    path('api/provinces/<int:pk>/', ProvinceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='province-detail'),

    # Kabupaten URLs
    path('api/kabupatens/', KabupatenViewSet.as_view({'get': 'list', 'post': 'create'}), name='kabupaten-list'),
    path('api/kabupatens/<int:pk>/', KabupatenViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='kabupaten-detail'),




    # Django Rest Framework API urls for link DRP 
    path("api/links/<str:province_code>/<str:kabupaten_code>/",views.LinksByProvinceKabupatenView.as_view(),name="links_by_province_kabupaten"),
    path("api/drp/<str:province_code>/<str:kabupaten_code>/<int:link_id>/",views.DRPByProvinceKabupatenLinkAPIView.as_view(),name="drp_by_province_kabupaten_link"),
    path('api/link-kabupaten/', LinkKabupatenListCreateView.as_view(), name='link_kabupaten_list_create'),
    path('api/link-kabupaten/<int:pk>/', LinkKabupatenDetailView.as_view(), name='link_kabupaten_detail'),

    # LinkKacematan Endpoints
    path('api/road-inventories/', RoadInventoryListCreateView.as_view(), name='roadinventory-list-create'),
    path('api/road-inventories/<int:pk>/', RoadInventoryDetailView.as_view(), name='roadinventory-detail'),
    path('api/link-kacematan/', LinkKacematanListCreateView.as_view(), name='link_kacematan_list_create'),
    path('api/link-kacematan/<int:pk>/', LinkKacematanDetailView.as_view(), name='link_kacematan_detail'),
    path('api/link-classes/<int:province_id>/<int:kabupaten_id>/',LinkClassListView.as_view(),name='linkclass-list'),
    # ConditionYear Routes
    path('api/condition_year/', ConditionYearListCreateView.as_view(), name="condition_year_list_create"),
    path('api/condition_year/<int:pk>/', ConditionYearRetrieveUpdateDeleteView.as_view(), name="condition_year_detail"),

    # RoadCondition Routes
    path('api/road_condition/', RoadConditionListCreateView.as_view(), name="road_condition_list_create"),
    path('api/road_condition/<int:pk>/', RoadConditionRetrieveUpdateDeleteView.as_view(), name="road_condition_detail"),
    
    # MCA criteria restapi urls 
    path('api/mca-criteria/', MCAcriteriaListCreateView.as_view(), name='mca-criteria-list-create'),
    path('api/mca-criteria/<int:pk>/', MCAcriteriaRetrieveUpdateDestroyView.as_view(), name='mca-criteria-detail'),

    # Culvert Inventory urls

    path('api/culvert-inventory/', views.culvert_inventory_view, name='culvert_inventory'),
    path('api/culvert-condition/form/', views.culvert_condition_form, name='culvert_condition_form'),
    path('api/culvert-condition/list/', views.culvert_condition_list, name='culvert_condition_list'),
    # Retaining walls
    
    path('api/retaining_walls/', views.retaining_walls_view, name='retaining_walls_view'),
    path('api/save_retaining_wall/', views.save_retaining_wall, name='save_retaining_wall'),
    path('api/save-wall-condition/', views.save_wall_condition, name='save_wall_condition'),
    path('api/display-wall-conditions/', views.display_wall_conditions, name='display_wall_conditions'),
        # OTP REGISTRATION on user email     
    #path('register/', views.registrationview, name='register'),
    #path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('api/register/', views.register_user, name='register_user'),
    path('api/verify-otp/', views.verify_otp, name='verify_otp'),
    path('api/login/', views.api_login, name='api-login'),
    path('api/pfid_dashboard/',views.pfid_dashboard, name= "pfid_dashboard_api"),
    path('api/balai_dashboard/', views.balai_dashboard, name='balai_dashboard_api'),
   
    path('api/province/', views.province_dashboard, name='province_dashboard'),
    #path('kabupaten/', views.kabupaten_dashboard, name='kabupaten_dashboard'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


