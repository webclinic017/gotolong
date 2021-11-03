from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class BrokerZerodhaTxn(models.Model):
    bzt_id = models.AutoField(primary_key=True)
    bzt_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bzt_tdate = models.DateField(blank=True, null=True)
    bzt_tsymbol = models.TextField(blank=True, null=True)
    bzt_exchange = models.TextField(blank=True, null=True)
    bzt_segment = models.TextField(blank=True, null=True)
    bzt_trade_type = models.IntegerField(blank=True, null=True)
    bzt_quantity = models.FloatField(blank=True, null=True)
    bzt_price = models.FloatField(blank=True, null=True)
    bzt_order_id = models.IntegerField(blank=True, null=True)
    bzt_trade_id = models.IntegerField(blank=True, null=True)
    bzt_order_exec_time = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'broker_zerodha_txn'
        unique_together = (('bzt_tsymbol', 'bzt_tdate'),)
