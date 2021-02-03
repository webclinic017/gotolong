# Create your models here.
from django.db import models


class Indices(models.Model):
    # index company name
    ind_name = models.TextField(primary_key=True)
    # index industry name
    ind_industry = models.TextField(blank=True, null=True)
    ind_ticker = models.TextField(blank=True, null=True)
    ind_series = models.TextField(blank=True, null=True)
    ind_isin = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_indices'
