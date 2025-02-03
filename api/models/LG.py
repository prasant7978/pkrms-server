from django.db import models

from api.models.Balai import Balai
from api.models.User import User


class LG(User):
    lgCode = models.CharField(max_length=5, unique=True, null=False)
    lgName = models.CharField(max_length=30, null=False)
    balai = models.ForeignKey(Balai, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'LG'