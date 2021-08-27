from django.db import models


# Create your models here.

class BrokerIcidirTxn(models.Model):
    bit_id = models.AutoField(primary_key=True)
    bit_stock_symbol = models.TextField(blank=True, null=True)
    bit_company_name = models.TextField(blank=True, null=True)
    bit_isin_code = models.TextField(blank=True, null=True)
    bit_action = models.TextField(blank=True, null=True)
    bit_quantity = models.IntegerField(blank=True, null=True)
    bit_txn_price = models.FloatField(blank=True, null=True)
    bit_brokerage = models.TextField(blank=True, null=True)
    bit_txn_charges = models.TextField(blank=True, null=True)
    bit_stamp_duty = models.TextField(blank=True, null=True)
    bit_segment = models.TextField(blank=True, null=True)
    bit_stt = models.TextField(blank=True, null=True)
    bit_remarks = models.TextField(blank=True, null=True)
    bit_txn_date = models.DateField(blank=True, null=True)
    bit_exchange = models.TextField(blank=True, null=True)
    bit_unused1 = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'broker_icidir_txn'
        unique_together = (('bit_company_name', 'bit_txn_date'),)
