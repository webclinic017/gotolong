# Create your models here.
from django.db import models


# Create your models here.

class Dividend(models.Model):
    divi_id = models.TextField(primary_key=True)
    divi_date = models.DateField(blank=True, null=True)
    divi_remarks = models.TextField(blank=True, null=True)
    divi_company = models.TextField(blank=True, null=True)
    divi_ticker = models.TextField(blank=True, null=True)
    divi_amount = models.TextField(blank=True, null=True)
    divi_score = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_dividend'
