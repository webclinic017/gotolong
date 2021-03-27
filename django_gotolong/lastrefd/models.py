# Create your models here.
from django.db import models

from time import strftime
from datetime import datetime


# Create your models here.

class Lastrefd(models.Model):
    lastrefd_module = models.TextField(primary_key=True)
    lastrefd_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'both_lastrefd'


def lastrefd_same(module_name):
    lastrefd_module = module_name
    e = Lastrefd.objects.get(lastrefd_module=lastrefd_module)
    lastrefd_date = e.lastrefd_date.strftime("%Y-%m-%d")
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    print("lastrefd_same: ", lastrefd_module, 'last: ', lastrefd_date, 'today: ', today_date)
    if lastrefd_date == today_date:
        return True
    else:
        return False


def lastrefd_update(module_name):
    now = datetime.now()
    lastrefd_module = module_name
    lastrefd_date = now.strftime("%Y-%m-%d %H:%M:%S")

    # delete existing record
    Lastrefd.objects.filter(lastrefd_module=lastrefd_module).delete()

    # update
    _, created = Lastrefd.objects.update_or_create(
        lastrefd_module=lastrefd_module,
        lastrefd_date=lastrefd_date
    )
