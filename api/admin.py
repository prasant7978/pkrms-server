from django.contrib import admin
from api.models.User import User, ApprovalRequest
from api.models.Province import Province
from api.models.Balai import Balai
from api.models.Kabupaten import Kabupaten
from api.models.Link import Link
from api.models.Role import Role
from api.models.roadCondition import RoadCondition
from api.models.roadInventory import RoadInventory 
from api.models.SysCode.drainCondition import DrainCondition
from api.models.SysCode.footpathCondition import FootPathCondition
from api.models.SysCode.impassable import Impassible
from api.models.SysCode.landUse import LandUse
from api.models.SysCode.linkClass import LinkClass
from api.models.SysCode.linkFunction import LinkFunction
from api.models.SysCode.linkStatus import LinkStatus
from api.models.SysCode.pavementType import PavementType
from api.models.SysCode.shoulderCondition import ShoulderCondition
from api.models.SysCode.shoulderType import ShoulderType
from api.models.SysCode.slopeCondition import SlopeCondition
from api.models.SysCode.terrain import Terrain




# Register your models here.
admin.site.register(User)
admin.site.register(ApprovalRequest)
admin.site.register(Province)
admin.site.register(Balai)
admin.site.register(Kabupaten)
admin.site.register(Link)
admin.site.register(Role)
admin.site.register(RoadCondition)
admin.site.register(RoadInventory)
admin.site.register(DrainCondition)
admin.site.register(FootPathCondition)
admin.site.register(Impassible)
admin.site.register(LandUse)
admin.site.register(LinkClass)
admin.site.register(LinkFunction)
admin.site.register(LinkStatus)
admin.site.register(PavementType)
admin.site.register(ShoulderCondition)
admin.site.register(ShoulderType)
admin.site.register(SlopeCondition)
admin.site.register(Terrain)
