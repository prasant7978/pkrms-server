from django.db import models
from api.models.Province import Province



class Balai(models.Model):
    balaiCode = models.CharField(max_length=5, unique=True, null=False)
    
    # Using string reference to avoid circular import issues
    provinceCode = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province code")
    
    balaiName = models.CharField(max_length=250, null=False)
    contactPerson = models.CharField(max_length=20)

    class Meta:
        db_table = 'Balai'

    
