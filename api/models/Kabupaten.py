from django.db import models

from api.models.Province import Province


class Kabupaten(models.Model):
    KabupatenCode = models.CharField(max_length=5, null=True, blank=True, default=None)
    KabupatenName = models.CharField(max_length=255, null=False)
    IslandCode = models.CharField(max_length=5, blank=True)
    DefaultKabupaten = models.BooleanField(default=False)
    Stable = models.IntegerField()
    Province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        db_table = 'kabupaten'

    def __str__(self):
        return self.KabupatenName