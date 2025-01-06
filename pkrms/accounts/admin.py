from django.contrib import admin
from .models import User, Role, Traffic_weighting_factors,Periodic_UnitCost, Traffic_volume,Retaining_walls_Condition, Province,Retaining_walls,CulvertInventory, MCAcriteria, ConditionYear,RoadCondition, Balai,  Kabupaten, Link, DRP , LinkClass, PriorityArea, CorridorName, LinkKabupaten, CorridorLink, LinkKacematan,RoadInventory

# Register all models using a loop
for model in [Province,Traffic_volume,Periodic_UnitCost, User, Role,
Retaining_walls_Condition,Retaining_walls,CulvertInventory, Balai,MCAcriteria, ConditionYear,
RoadCondition, Kabupaten,Traffic_weighting_factors,Link, DRP,LinkClass,PriorityArea, CorridorName , LinkKabupaten, CorridorLink,
LinkKacematan,RoadInventory]:
    admin.site.register(model)


# Register your models here.
