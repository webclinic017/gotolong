# Create your models here.
from django.db import models


class Fof(models.Model):
    # index company name
    fof_scheme = models.TextField(primary_key=True)
    fof_type = models.TextField(blank=True, null=True)
    # index industry name
    fof_benchmark = models.TextField(blank=True, null=True)
    fof_aum = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'global_fof'
