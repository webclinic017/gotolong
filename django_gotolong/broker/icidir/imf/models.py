# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import User

class BrokerIcidirMf(models.Model):
    bim_id = models.IntegerField(blank=True, null=True)
    bim_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bim_amc = models.TextField(blank=True, null=True)
    bim_name = models.TextField(primary_key=True)
    bim_category = models.TextField(blank=True, null=True)
    bim_subcat = models.TextField(blank=True, null=True)
    bim_rating = models.TextField(blank=True, null=True)
    bim_units = models.FloatField(blank=True, null=True)
    bim_acp = models.FloatField(blank=True, null=True)
    bim_cost_value = models.FloatField(blank=True, null=True)
    bim_nav_date = models.TextField(blank=True, null=True)
    bim_nav = models.FloatField(blank=True, null=True)
    bim_nav_value = models.FloatField(blank=True, null=True)
    bim_pnl_realized = models.FloatField(blank=True, null=True)
    bim_pnl = models.FloatField(blank=True, null=True)
    bim_pnl_pct = models.FloatField(blank=True, null=True)
    bim_research_reco = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'broker_icidir_mf'
