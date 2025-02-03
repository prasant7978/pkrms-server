from django.db import models

from api.models.Kabupaten import Kabupaten
from api.models.Province import Province

class Link(models.Model):
    linkNo = models.CharField(unique=True,null=False)
    linkCode = models.CharField(unique=True, null= False)
    linkName = models.CharField(max_length=50)
    linkLengthOfficial = models.FloatField()
    linkLengthActual = models.FloatField()
    province = models.ForeignKey(Province,on_delete=models.CASCADE,null= False)
    kabupaten = models.ForeignKey(Kabupaten,on_delete=models.CASCADE,null=False)
    