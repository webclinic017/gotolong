from django.db import models


# Create your models here.

class Bhav(models.Model):
    bhav_ticker = models.TextField(primary_key=True)
    bhav_price = models.TextField(blank=True, null=True)
    bhav_isin = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_bhav'
