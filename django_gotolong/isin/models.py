# Create your models here.
from django.db import models


class Isin(models.Model):
    comp_name = models.TextField(primary_key=True)
    comp_industry = models.TextField(blank=True, null=True)
    comp_ticker = models.TextField(blank=True, null=True)
    series = models.TextField(blank=True, null=True)
    comp_isin = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_isin'
