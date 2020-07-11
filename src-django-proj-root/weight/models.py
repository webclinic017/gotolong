# Create your models here.
from django.db import models


# Create your models here.

class Weight(models.Model):
    cap_type = models.TextField(primary_key=True)
    cap_weight = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'global_weight'
