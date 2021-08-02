from django.db import models


# Create your models here.

class DematTxn(models.Model):
    dt_id = models.AutoField(primary_key=True)
    dt_broker = models.TextField(blank=True, null=True)
    dt_ticker = models.TextField(blank=True, null=True)
    dt_isin = models.TextField(blank=True, null=True)
    dt_action = models.TextField(blank=True, null=True)
    dt_quantity = models.IntegerField(blank=True, null=True)
    dt_price = models.FloatField(blank=True, null=True)
    dt_amount = models.FloatField(blank=True, null=True)
    dt_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'user_demat_txn'
        unique_together = (('dt_ticker', 'dt_date'),)
