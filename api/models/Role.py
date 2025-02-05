from django.db import models

class Role(models.Model):
    SUPERADMIN = 'superadmin'
    PFID = 'pfid'
    BALAI_LG = 'balai_lg'
    PROVINCIAL_LG = 'provience_lg'
    KABUPATEN_LG = 'kabupaten_lg'

    ROLE_CHOICES = [
        (SUPERADMIN, 'Super Admin'),
        (PFID, 'PFID'),
        (BALAI_LG, 'Balai LG'),
        (PROVINCIAL_LG, 'Provincial LG'),
        (KABUPATEN_LG, 'Kabupaten LG'),
    ]

    role_name = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=PFID,
        verbose_name="Role",
        unique=True,
    )

    def __str__(self):
        return self.role_name