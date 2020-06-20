from django.db import models

# Create your models here.
from django.db import models


class Amfi(models.Model):
    sno = models.TextField(primary_key=True)
    company_name = models.TextField(blank=True, null=True)
    isin = models.TextField(blank=True, null=True)
    bse_symbol = models.TextField(blank=True, null=True)
    nse_symbol = models.TextField(blank=True, null=True)
    avg_mcap = models.TextField(blank=True, null=True)
    cap_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amfi'
