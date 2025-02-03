from django.db import models

from api.models import User

class PFID(User):
    pfidCode = models.CharField(max_length=5, unique=True, null=False)
    name = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'PFID'