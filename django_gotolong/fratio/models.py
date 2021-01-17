# Create your models here.
from django.db import models


# Create your models here.

class Fratio(models.Model):
    fratio_name = models.TextField(primary_key=True)
    fratio_buy = models.FloatField(blank=True, null=True)
    fratio_hold = models.FloatField(blank=True, null=True)
    fratio_enabled = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'global_fratio'
