from django.db import models

# Create your models here.
from django.db import models


class Dividend(models.Model):
    id = models.TextField(primary_key=True)
    date = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    amount = models.TextField(blank=True, null=True)
    comp_name = models.TextField(blank=True, null=True)
    ticker = models.TextField(blank=True, null=True)
    isin = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dividend'
