# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from amfi.models import Amfi


class DematSum(models.Model):
    stock_symbol = models.TextField(blank=True, null=True)
    comp_name = models.TextField(primary_key=True)
    # isin_code = models.TextField(blank=True, null=True)
    isin_code = models.ForeignKey(Amfi, on_delete=models.DO_NOTHING)
    qty = models.IntegerField(blank=True, null=True)
    acp = models.FloatField(blank=True, null=True)
    cmp = models.TextField(blank=True, null=True)
    pct_change = models.TextField(blank=True, null=True)
    value_cost = models.FloatField(blank=True, null=True)
    value_market = models.FloatField(blank=True, null=True)
    days_gain = models.TextField(blank=True, null=True)
    days_gain_pct = models.TextField(blank=True, null=True)
    realized_pl = models.TextField(blank=True, null=True)
    unrealized_pl = models.TextField(blank=True, null=True)
    unrealized_pl_pct = models.TextField(blank=True, null=True)
    unused1 = models.TextField(blank=True, null=True)

    # amfis = models.ManyToManyField(Amfi)

    class Meta:
        db_table = 'user_demat_sum'
