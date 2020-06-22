from django.db import models


# Create your models here.

class Nach(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    ticker = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nach'
