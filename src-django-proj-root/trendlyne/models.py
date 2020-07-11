from django.db import models


# Create your models here.

class Trendlyne(models.Model):
    stock_name = models.TextField(blank=True, null=True)
    isin = models.TextField(primary_key=True)
    bat = models.IntegerField(blank=True, null=True)
    der = models.FloatField(blank=True, null=True)
    roce3 = models.FloatField(blank=True, null=True)
    dpr2 = models.FloatField(blank=True, null=True)
    sales2 = models.FloatField(blank=True, null=True)
    profit5 = models.FloatField(blank=True, null=True)
    icr = models.FloatField(blank=True, null=True)
    pledge = models.FloatField(blank=True, null=True)
    low_3y = models.FloatField(blank=True, null=True)
    low_5y = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'global_trendlyne'
