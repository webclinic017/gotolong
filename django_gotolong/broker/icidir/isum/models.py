# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django_gotolong.amfi.models import Amfi


class BrokerIcidirSum(models.Model):
    bis_stock_symbol = models.TextField(blank=True, null=True)
    bis_company_name = models.TextField(primary_key=True)
    # isin_code = models.TextField(blank=True, null=True)
    bis_isin_code = models.ForeignKey(Amfi, on_delete=models.DO_NOTHING)
    bis_qty = models.IntegerField(blank=True, null=True)
    bis_acp = models.FloatField(blank=True, null=True)
    bis_cmp = models.TextField(blank=True, null=True)
    bis_pct_change = models.TextField(blank=True, null=True)
    bis_value_cost = models.FloatField(blank=True, null=True)
    bis_value_market = models.FloatField(blank=True, null=True)
    bis_days_gain = models.TextField(blank=True, null=True)
    bis_days_gain_pct = models.TextField(blank=True, null=True)
    bis_realized_pl = models.TextField(blank=True, null=True)
    bis_unrealized_pl = models.TextField(blank=True, null=True)
    bis_unrealized_pl_pct = models.TextField(blank=True, null=True)
    bis_unused1 = models.TextField(blank=True, null=True)

    # amfis = models.ManyToManyField(Amfi)

    class Meta:
        db_table = 'broker_icidir_sum'


def broker_idirect_sum_load_stocks(brokersum_list):
    # load list of demat symbols
    for brokersum in BrokerIcidirSum.objects.all():
        brokersum_list.append(brokersum.stock_symbol)
