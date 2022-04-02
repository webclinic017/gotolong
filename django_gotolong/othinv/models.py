# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

othinv_choices = [('PF-GPF', 'PF-GPF'),
                  ('PPF', 'PPF'),
                  ('NPS-T1', 'NPS-T1'),
                  ('NPS-T2', 'NPS-T2'),
                  ('MF', 'MF'),
                  ('SSY', 'SSY'),
                  ('SGB', 'SGB'),
                  ('Demat', 'Demat'),
                  ('Plot', 'Plot'),
                  ('House', 'House'),
                  ('RSU-Vested', 'RSU-Vested'),
                  ('Gratuity', 'Gratuity'),
                  ('Other', 'Other')
                  ]


class Othinv(models.Model):
    othinv_id = models.AutoField(primary_key=True)
    othinv_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    othinv_name = models.TextField(choices=othinv_choices)
    othinv_details = models.TextField(blank=True, null=True)
    othinv_equity = models.FloatField(blank=True, null=True)
    othinv_debt = models.FloatField(blank=True, null=True)
    othinv_gold = models.FloatField(blank=True, null=True)
    othinv_intl = models.FloatField(blank=True, null=True)
    othinv_realty = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = u'user_othinv'

    def __unicode__(self):
        return u'%s ' % (self.othinv_name)

    def get_update_url(self):
        return reverse('othinv-update', args=(self.othinv_id,))

    def get_add_url(self):
        return reverse('othinv-add')
