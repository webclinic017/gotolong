# Create your models here.
from django.db import models


# Create your models here.

class Gfundareco(models.Model):
    funda_reco_ticker = models.TextField(primary_key=True)
    funda_reco_isin = models.TextField(blank=True, null=True)
    funda_reco_type = models.TextField(blank=True, null=True)
    funda_reco_cause = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_funda_reco'
