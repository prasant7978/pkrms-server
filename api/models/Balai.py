from django.db import models

from api.models import User

class Balai(User):
    balaiCode = models.CharField(max_length=5, unique=True, null=False)
    balaiName = models.CharField(max_length=30, null=False)
    contactPerson = models.CharField(max_length=20)

    class Meta:
        db_table = 'Balai'