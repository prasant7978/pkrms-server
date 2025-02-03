from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from api.views.ProvinceView import ProvinceView # type: ignore


router = DefaultRouter()
router.register(r'province',ProvinceView)



urlpatterns = [
    path('admin/',admin.site.urls),
    path('', include(router.urls))
]