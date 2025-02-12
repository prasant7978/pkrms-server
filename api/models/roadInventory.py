from django.db import models
from api.models.Link import Link
from api.models.SysCode.drainType import DrainType
from api.models.SysCode.impassable import Impassible
from api.models.SysCode.landUse import LandUse
from api.models.SysCode.shoulderType import ShoulderType
from api.models.SysCode.terrain import Terrain




class RoadInventory(models.Model):
    roadInventoryId = models.CharField(primary_key=True, null=False)
    linkId = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='road_inventory')
    linkNo = models.BigIntegerField(null=True, blank=True)
    chainageFrom = models.IntegerField(null=True, blank=True)
    chainageTo = models.IntegerField(null=True, blank=True)
    drpFrom = models.IntegerField(null=True, blank=True)
    offsetFrom = models.IntegerField(null=True, blank=True)
    drpTo = models.IntegerField(null=True, blank=True)
    offsetTo = models.IntegerField(null=True, blank=True)
    paveWidth = models.FloatField(null=True, blank=True)
    row = models.IntegerField(null=True, blank=True)
    paveType = models.IntegerField(null=True, blank=True)  
    shoulderWidthL = models.FloatField(null=True, blank=True)
    shoulderWidthR = models.FloatField(null=True, blank=True)
    
    shoulderTypeL = models.ForeignKey(
        ShoulderType, 
        on_delete=models.CASCADE, 
        related_name='road_inventory_left', null=True , blank=True
    )
    shoulderTypeR = models.ForeignKey(
        ShoulderType, 
        on_delete=models.CASCADE, 
        related_name='road_inventory_right', null=True , blank=True
    )

    drainTypeL = models.ForeignKey(
        DrainType, 
        on_delete=models.CASCADE, 
        related_name='road_inventory_left', null=True , blank=True
    )
    drainTypeR = models.ForeignKey(
        DrainType, 
        on_delete=models.CASCADE, 
        related_name='road_inventory_right', null=True , blank=True
    )

    terrain = models.ForeignKey(
        Terrain, 
        on_delete=models.CASCADE, 
        related_name='road_inventory', null=True , blank=True
    )

    landUseL = models.ForeignKey(
        LandUse, 
        on_delete=models.CASCADE, 
        related_name='road_inventory_left', null=True , blank=True
    )
    landUseR = models.ForeignKey(
        LandUse, 
        on_delete=models.CASCADE, 
        related_name='road_inventory_right', null=True , blank=True
    )

    impassable = models.BooleanField()
    impassableReason = models.ForeignKey(
        Impassible, 
        on_delete=models.CASCADE, 
        related_name='road_inventory', null=True , blank=True
    )

    class Meta:
        db_table = 'RoadInventory'  # Standardized table name
