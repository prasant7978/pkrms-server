from django.db import models

class SlopeCondition(models.Model):
    code = models.CharField(null=True, blank=True)
    codeDescriptionEng = models.CharField(max_length=50,null=True, blank=True)
    codeDescriptionInd = models.CharField(max_length=50,null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'SlopeCondition'