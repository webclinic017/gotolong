from django.db import models


# Create your models here.

class Nach(models.Model):
    name = models.TextField(primary_key=True)
    ticker = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_nach'
