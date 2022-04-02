# Create your models here.
from django.db import models


class Fofeti(models.Model):
    # index company name
    fofeti_scheme = models.TextField(primary_key=True)
    fofeti_type = models.TextField(blank=True, null=True)
    # index industry name
    fofeti_benchmark = models.TextField(blank=True, null=True)
    fofeti_aum = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'global_fofeti'
