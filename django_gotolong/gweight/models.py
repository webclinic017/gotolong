# Create your models here.
from django.db import models


# Create your models here.

class Gweight(models.Model):
    gw_cap_type = models.TextField(primary_key=True)
    gw_cap_weight = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'global_weight'
