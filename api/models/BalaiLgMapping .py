from django.db import models

from api.models import LG, Balai, Kabupaten, Province

class BalaiLGMapping(models.Model):
    balai = models.ForeignKey(Balai, on_delete=models.CASCADE, null=True, blank=True)
    lg = models.ForeignKey(LG, on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['balai', 'lg', 'province', 'kabupaten'], 
                name='unique_balai_lg_province_kabupaten'
            )
        ]

    def __str__(self):
        return f"Balai: {self.balai}, LG: {self.lg}, Province: {self.province}, Kabupaten: {self.kabupaten}"
