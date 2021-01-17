# Create your models here.
from django.db import models


# Create your models here.

class Greco(models.Model):
    reco_ticker = models.TextField(primary_key=True)
    reco_isin = models.TextField(blank=True, null=True)
    reco_type = models.TextField(blank=True, null=True)
    reco_cause = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_reco'
