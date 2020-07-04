from django.db import models

# Create your models here.
from django.db import models



class Dividend(models.Model):
    # id = models.TextField(primary_key=True)
    div_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(primary_key=True)
    amount = models.TextField(blank=True, null=True)
    ticker = models.TextField(blank=True, null=True)
    isin = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_dividend'
