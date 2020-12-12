from django.db import models


# Create your models here.

class Ftwhl(models.Model):
    ftwhl_ticker = models.TextField(primary_key=True)
    ftwhl_high = models.TextField(blank=True, null=True)
    ftwhl_high_dt = models.TextField(blank=True, null=True)
    ftwhl_low = models.TextField(blank=True, null=True)
    ftwhl_low_dt = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_ftwhl'
