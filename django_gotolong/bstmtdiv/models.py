# Create your models here.
from django.db import models

from django.contrib.auth.models import User

class BstmtDiv(models.Model):
    bsdiv_id = models.TextField(primary_key=True)
    bsdiv_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bsdiv_date = models.DateField(blank=True, null=True)
    bsdiv_remarks = models.TextField(blank=True, null=True)
    bsdiv_amount = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_bstmt_div'
        managed = False
