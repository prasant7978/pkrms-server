from django.db import models

class Role(models.Model):
    
    PFID = 'pfid'
    DPSI = 'dpsi'
    SPDJD = "spdjd"
    BALAI = 'balai'
    PROVINCIAL_LG = 'province_lg'
    KABUPATEN_LG = 'kabupaten_lg'

    ROLE_CHOICES = [
        
        (PFID, 'PFID'),
        (DPSI, 'DPSI'),
        (SPDJD, 'SPDJD'),
        (BALAI, 'Balai '),
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
    
    
    
    
    



