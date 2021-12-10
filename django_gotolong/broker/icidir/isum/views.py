# Create your views here.

from .models import BrokerIcidirSum

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.list import ListView

from django.db.models import OuterRef, Subquery, Count, Sum, Max, Min
from django.db.models.functions import Trim, Lower, Round

from django_gotolong.amfi.models import Amfi
from django_gotolong.gfundareco.models import Gfundareco

import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun

class BrokerIcidirSumListView(ListView):
    model = BrokerIcidirSum

    # if pagination is desired
    # paginate_by = 300

    def get_queryset(self):
        return BrokerIcidirSum.objects.all().filter(bis_user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# one parameter named request
def BrokerIcidirSumUpload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    template = "invalid-get-request.html"
    # change column name of data frame
    columns_list = ['bis_stock_symbol', 'bis_company_name', 'bis_isin_code_id', 'bis_qty', 'bis_acp',
                    'bis_cmp', 'bis_pct_change', 'bis_value_cost', 'bis_value_market',
                    'bis_days_gain', 'bis_days_gain_pct', 'bis_realized_pl', 'bis_unrealized_pl',
                    'bis_unrealized_pl_pct', 'bis_unused1']
    list_url_name = "broker-icidir-sum-list"
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name)

    # delete existing records
    print('Deleted existing BrokerIcidirSum data')
    BrokerIcidirSum.objects.all().filter(bis_user_id=request.user.id).delete()

    max_id_instances = BrokerIcidirSum.objects.aggregate(max_id=Max('bis_id'))
    max_id = max_id_instances['max_id']
    print('max_id ', max_id)
    if max_id is None:
        max_id = 0
        print('max_id ', max_id)

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)
    unique_id = max_id
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        unique_id += 1
        column[0] = column[0].strip()
        column[1] = column[1].strip()

        _, created = BrokerIcidirSum.objects.update_or_create(
            bis_id=unique_id,
            bis_user_id=request.user.id,
            bis_stock_symbol=column[0],
            bis_company_name=column[1],
            bis_isin_code_id=column[2],
            bis_qty=column[3],
            bis_acp=column[4],
            bis_cmp=column[5],
            bis_pct_change=column[6],
            bis_value_cost=column[7],
            bis_value_market=column[8],
            bis_days_gain=column[9],
            bis_days_gain_pct=column[10],
            bis_realized_pl=column[11],
            bis_unrealized_pl=column[12],
            bis_unrealized_pl_pct=column[13],
            bis_unused1=column[14]
        )

    lastrefd_update("broker-icidir-sum")

    print('Completed loading new BrokerIcidirSum data')
    return HttpResponseRedirect(reverse(list_url_name))

def BrokerIcidirSumReset(request):
    # delete existing records
    print('Cleared existing BrokerIcidirSum data')
    BrokerIcidirSum.objects.all().filter(bis_user_id=request.user.id).delete()
    return HttpResponseRedirect(reverse("broker-icidir-sum-list"))
