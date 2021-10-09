# Create your models here.
from django.db import models
from django.urls import reverse

class Fratio(models.Model):
    fratio_name = models.TextField(primary_key=True)
    fratio_buy = models.FloatField(blank=True, null=True)
    fratio_hold = models.FloatField(blank=True, null=True)
    fratio_enabled = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = u'global_fratio'

    def __unicode__(self):
        return u'%s ' % (self.fratio_name)

    # deprecated - @models.permalink
    def get_update_url(self):
        return reverse('fratio-update', args=(self.fratio_name,))

    def get_add_url(self):
        return reverse('fratio-add')
