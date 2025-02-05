from django.db import models

class Province(models.Model):
    provinceCode = models.CharField(max_length=10, unique=True, null=False)
    provinceName = models.CharField(max_length=50)
    defaultProvince = models.BooleanField(default=False)
    stable = models.IntegerField()

    class Meta:
        db_table = "Province"  # Explicitly setting the table name

    def __str__(self):
        return self.provinceName