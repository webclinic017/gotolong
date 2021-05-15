# Create your models here.
from django.db import models


class Mfund(models.Model):
    # index company name
    mfund_scheme = models.TextField(primary_key=True)
    mfund_type = models.TextField(blank=True, null=True)
    # index industry name
    mfund_benchmark = models.TextField(blank=True, null=True)
    mfund_aum = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'global_mfund'
