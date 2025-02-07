from django.db import models

from api.models.SysCode.drainType import DrainType
from api.models.SysCode.impassable import Impassible
from api.models.SysCode.landUse import LandUse
from api.models.SysCode.shoulderType import ShoulderType
from api.models.SysCode.terrain import Terrain


class RoadInventory(models.Model):
    provinceCode = models.IntegerField()
    kabupatenCode = models.IntegerField()
    linkNo = models.BigIntegerField()
    chainageFrom = models.IntegerField()
    chainageTo = models.IntegerField()
    drpFrom = models.IntegerField()
    offsetFrom = models.IntegerField()
    drpTo = models.IntegerField()
    offsetTo = models.IntegerField()
    paveWidth = models.FloatField()
    row = models.IntegerField()
    paveType = models.IntegerField()  
    shoulderWidthL = models.FloatField()
    shoulderWidthR = models.FloatField()
    shoulderTypeL = models.ForeignKey(ShoulderType, on_delete=models.CASCADE)
    shoulderTypeR = models.IntegerField(ShoulderType, ondelete=models.CASCADE)
    drainTypeL = models.ForeignKey(DrainType, on_delete= models.CASCADE)
    drainTypeR = models.ForeignKey(DrainType, on_delete= models.CASCADE)
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)
    landUseL = models.ForeignKey(LandUse, on_delete=models.CASCADE)
    landUseR = models.ForeignKey(LandUse, on_delete=models.CASCADE)
    impassable = models.BooleanField()
    impassableReason = models.ForeignKey(Impassible, on_delete=models.CASCADE)


    class Meta:
        db_table = 'RoadInventory'
        