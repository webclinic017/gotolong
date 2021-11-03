# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django_gotolong.amfi.models import Amfi

from django.contrib.auth.models import User


class BrokerZerodhaSum(models.Model):
    bzs_id = models.IntegerField(blank=True, null=True)
    bzs_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bzs_instrument = models.TextField(primary_key=True)
    bzs_quantity = models.IntegerField(blank=True, null=True)
    bzs_average_cost = models.FloatField(blank=True, null=True)
    bzs_ltp = models.TextField(blank=True, null=True)
    bzs_cur_value = models.FloatField(blank=True, null=True)
    bzs_pnl = models.FloatField(blank=True, null=True)
    bzs_net_chg = models.FloatField(blank=True, null=True)
    bzs_day_chg = models.FloatField(blank=True, null=True)

    # amfis = models.ManyToManyField(Amfi)

    class Meta:
        db_table = 'broker_zerodha_sum'


def broker_idirect_sum_load_stocks(brokersum_list):
    # load list of demat symbols
    for brokersum in BrokerZerodhaSum.objects.all():
        brokersum_list.append(brokersum.bzs_instrument)