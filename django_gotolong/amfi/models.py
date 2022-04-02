from django.db import models


# Create your models here.

class Amfi(models.Model):
    comp_rank = models.IntegerField(blank=True, null=True)
    comp_name = models.TextField(primary_key=True)
    comp_isin = models.TextField(blank=True, null=True)
    bse_symbol = models.TextField(blank=True, null=True)
    nse_symbol = models.TextField(blank=True, null=True)
    avg_mcap = models.TextField(blank=True, null=True)
    cap_type = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'global_amfi'


def amfi_load_rank(amfi_rank_dict):
    # load amfi ranks
    for amfi in Amfi.objects.all():
        amfi_rank_dict[amfi.nse_symbol] = amfi.comp_rank
        if amfi.nse_symbol != amfi.bse_symbol:
            amfi_rank_dict[amfi.bse_symbol] = amfi.comp_rank
