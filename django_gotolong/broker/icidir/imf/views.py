# Create your views here.

from .models import BrokerIcidirMf

from django.views.generic.list import ListView

from django.db.models import IntegerField, F, ExpressionWrapper, fields, Max, Min, Sum, Count

from django.urls import reverse
from django.http import HttpResponseRedirect
import urllib3
import csv
import io

import re

import openpyxl

import pandas as pd

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.tools import make_subplots


class BrokerIcidirMfListView(ListView):
    model = BrokerIcidirMf

    def get_queryset(self):
        queryset = BrokerIcidirMf.objects.all().filter(bim_user_id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        refresh_url = BrokerIcidirMf_url()
        context["refresh_url"] = refresh_url
        return context


def BrokerIcidirMf_url():
    url = 'https://archives.nseindia.com/content/BrokerIcidirMf/ind_nifty500list.csv'

    return url


# one parameter named request
def BrokerIcidirMf_fetch(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()
    debug_level = 1
    print('fetch not supported')
    return HttpResponseRedirect(reverse("imf-list"))

# one parameter named request
def BrokerIcidirMf_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    template = "imf/BrokerIcidirMf_list.html"
    # change column name of data frame
    columns_list = ["amc", "name", "category", "subcat", "rating",
                    "units", "acp", "cost_value",
                    "nav_date", "nav", "nav_value",
                    "pnl_realized", "pnl", "pnl_pct",
                    "research_reco"]
    list_url_name = "imf-list"
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name)

    # delete existing records
    print('Deleted existing BrokerIcidirMf data')
    BrokerIcidirMf.objects.all().filter(bim_user_id=request.user.id).delete()

    # note: what about using existing slots... how do we fill holes
    #
    max_id_instances = BrokerIcidirMf.objects.aggregate(max_id=Max('bim_id'))
    max_id = max_id_instances['max_id']
    print('max_id ', max_id)
    if max_id is None:
        max_id = 0
        print('max_id ', max_id)

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    # skip top 1 row
    next(io_string)

    skip_records = 0
    unique_id = max_id
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        unique_id += 1
        bim_user_id = request.user.id
        bim_amc = column[0].strip()
        bim_name = column[1].strip()
        bim_category = column[2].strip()
        bim_subcat = column[3].strip()
        bim_rating = column[4].strip()
        bim_units = column[5].strip()
        bim_acp = column[6].strip()
        bim_cost_value = column[7].strip()
        bim_nav_date = column[8].strip()
        bim_nav = column[9].strip()
        bim_nav_value = column[10].strip()
        bim_pnl_realized = column[10].strip()
        bim_pnl = column[12].strip()
        bim_pnl_pct = column[13].strip()
        bim_research_reco = column[14].strip()

        # print('bim_units ', bim_units)
        # skip mutual funds with 0 holdings
        # if int(float(bim_units)) !=  0 :

        _, created = BrokerIcidirMf.objects.update_or_create(
            bim_id=unique_id,
            bim_user_id=bim_user_id,
            bim_amc=bim_amc,
            bim_name=bim_name,
            bim_category=bim_category,
            bim_subcat=bim_subcat,
            bim_rating=bim_rating,
            bim_units=bim_units,
            bim_acp=bim_acp,
            bim_cost_value=bim_cost_value,
            bim_nav_date=bim_nav_date,
            bim_nav=bim_nav,
            bim_nav_value=bim_nav_value,
            bim_pnl_realized=bim_pnl_realized,
            bim_pnl=bim_pnl,
            bim_pnl_pct=bim_pnl_pct,
            bim_research_reco=bim_research_reco
        )

    lastrefd_update("imf")

    print('Skipped records', skip_records)
    print('Completed loading new BrokerIcidirMf data')
    return HttpResponseRedirect(reverse(list_url_name))
