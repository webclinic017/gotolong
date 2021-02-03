# Create your models here.
from django.db import models

from time import strftime


# Create your models here.

class Lastrefd(models.Model):
    lastrefd_module = models.TextField(primary_key=True)
    lastrefd_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'both_lastrefd'


def lastrefd_update(module_name):
    lastrefd_module = module_name
    lastrefd_date = strftime("%Y-%m-%d")
    _, created = Lastrefd.objects.update_or_create(
        lastrefd_module=lastrefd_module,
        lastrefd_date=lastrefd_date
    )
