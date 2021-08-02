from django.db import models


# Create your models here.

class BrokerIcidirTxn(models.Model):
    dt_id = models.AutoField(primary_key=True)
    stock_symbol = models.TextField(blank=True, null=True)
    comp_name = models.TextField(blank=True, null=True)
    isin_code = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    txn_price = models.FloatField(blank=True, null=True)
    brokerage = models.TextField(blank=True, null=True)
    txn_charges = models.TextField(blank=True, null=True)
    stamp_duty = models.TextField(blank=True, null=True)
    segment = models.TextField(blank=True, null=True)
    stt = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    txn_date = models.DateField(blank=True, null=True)
    exchange = models.TextField(blank=True, null=True)
    unused1 = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'broker_icidir_txn'
        unique_together = (('comp_name', 'txn_date'),)
