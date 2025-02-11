from django.contrib import admin
from .models import User, Role, Traffic_weighting_factors, Traffic_volume,Retaining_walls_Condition, Province,Retaining_walls,CulvertInventory, RoadCondition, Balai,  Kabupaten, Link, DRP , LinkClass, PriorityArea,  LinkKabupaten, LinkKacematan,RoadInventory

# Register all models using a loop
for model in [Province,Traffic_volume, User, Role,
Retaining_walls_Condition,Retaining_walls,CulvertInventory, Balai,
RoadCondition, Kabupaten,Traffic_weighting_factors,Link, DRP,LinkClass,PriorityArea, LinkKabupaten,
LinkKacematan,RoadInventory]:
    admin.site.register(model)


# Register your models here.
