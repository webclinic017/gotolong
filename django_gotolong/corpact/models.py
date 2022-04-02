from django.db import models


# Create your models here.

class Corpact(models.Model):
    ca_ticker = models.TextField(primary_key=True)
    ca_total = models.IntegerField(blank=True, null=True)
    ca_bonus = models.IntegerField(blank=True, null=True)
    ca_buyback = models.IntegerField(blank=True, null=True)
    ca_dividend = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'global_corpact'
