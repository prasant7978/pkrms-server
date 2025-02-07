from django.db import models

class ShoulderType(models.Model):
    code = models.CharField()
    codeDescriptionEng = models.CharField(max_length=50)
    codeDescriptionInd = models.CharField(max_length=50)
    order = models.IntegerField()
    
    class Meta:
        db_table = 'ShouderType'