from django.db import models

# Create your models here.
from django.db import models


class Amfi(models.Model):
    comp_rank = models.IntegerField(blank=True, null=True)
    comp_name = models.TextField(primary_key=True)
    comp_isin = models.TextField(blank=True, null=True)
    bse_symbol = models.TextField(blank=True, null=True)
    nse_symbol = models.TextField(blank=True, null=True)
    avg_mcap = models.TextField(blank=True, null=True)
    cap_type = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_amfi'
