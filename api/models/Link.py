from django.db import models

from api.models.Kabupaten import Kabupaten
from api.models.Province import Province
from api.models.SysCode.linkClass import LinkClass
from api.models.SysCode.linkFunction import LinkFunction
from api.models.SysCode.linkStatus import LinkStatus

class Link(models.Model):
    linkId = models.CharField(primary_key=True,null= False) # provinceCode-kabupatenCode-linkNo 
    linkNo = models.CharField(unique=True,null=False)
    linkCode = models.CharField(unique=True, null= False)
    linkName = models.CharField(max_length=100, null=True, blank=True)
    linkLengthOfficial = models.FloatField(null=True, blank=True)
    linkLengthActual = models.FloatField(null=True, blank=True)
    # status = models.ForeignKey(LinkStatus,on_delete=models.CASCADE, null=True, blank=True)  # link status
    # function = models.ForeignKey(LinkFunction,on_delete=models.CASCADE, null=True, blank=True)  # link function
    # class_field = models.ForeignKey(LinkClass,on_delete=models.CASCADE, db_column='class',null=True, blank=True)  # Link class
    status = models.CharField(unique=True, null= False)
    function = models.CharField(unique=True, null= False)
    class_field = models.CharField(unique=True, null= False)
    wti = models.IntegerField(null=True, blank=True)
    mca2 = models.IntegerField(null=True, blank=True)
    mca3 = models.IntegerField(null=True, blank=True)
    mca4 = models.IntegerField(null=True, blank=True)
    mca5 = models.IntegerField(null=True, blank=True)
    projectNumber = models.CharField(null=True, blank=True)
    cumesa = models.FloatField(null=True, blank=True)
    esa0 = models.FloatField(null=True, blank=True)
    aadt = models.IntegerField(null=True, blank=True)
    accessStatus = models.CharField(null=True, blank=True)
    inbound = models.CharField(null=True, blank=True) # extra attribute
    
    province = models.ForeignKey(Province,on_delete=models.CASCADE,null=True,blank=True)
    # kabupaten = models.ForeignKey(Kabupaten,on_delete=models.CASCADE, null=True,blank=True)
    # province = models.CharField(unique=True, null= False)
    kabupaten = models.CharField(unique=True, null= False)
    

    class Meta:
        db_table = 'link'