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

    debug_level = 1
    # declaring template
    template = "imf/BrokerIcidirMf_list.html"
    data = BrokerIcidirMf.objects.all()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)

    req_file = request.FILES['file']

    # let's check if it is a csv file

    if req_file.name.endswith('.xls') or req_file.name.endswith('.xlsx'):
        # get worksheet name
        # print('temporary file path:', req_file.temporary_file_path)
        print(req_file)

        if True:
            wb = openpyxl.load_workbook(req_file)
            print(wb.sheetnames)
            sheet_name = wb.sheetnames[0]
            print(sheet_name)
            ws = wb[sheet_name]
            df = pd.DataFrame(ws.values)
        else:
            xl = pd.ExcelFile(req_file)
            if debug_level > 0:
                print(xl.sheet_names)
            # single worksheet - Data
            sheet_name = xl.sheet_names[0]
            df = xl.parse(sheet_name)

        # can be 'Data'
        # can be 'Average MCap Jan Jun 2020'
        # if sheet_name != 'fund-performance':
        #    print("sheet name changed to", sheet_name)

        # ignore top 6 line : Value Research, Fund Performance
        # remove top six line from dataframe
        # ignore the top 1 line
        # df = df.iloc[1:]

        if debug_level > 0:
            print("old columns : ")
            print(df.columns)

        # change column name of data frame
        columns_list = ["amc", "name", "category", "subcat", "rating",
                        "units", "acp", "cost_value",
                        "nav_date", "nav", "nav_value",
                        "pnl_realized", "pnl", "pnl_pct",
                        "research_reco"]

        df.columns = columns_list

        if debug_level > 0:
            print("new columns : ")
            print(df.columns)

        # Keep only top 1000 entries
        # df = df.iloc[:1000]

        # round avg_mcap
        # df = df.round({'avg_mcap' : 1})
        # covert to numeric
        # df[["avg_mcap"]] = df[["avg_mcap"]].apply(pd.to_numeric)
        df[["daily_aum"]] = df[["daily_aum"]].astype(int)

        # drop columns that are not required
        skip_columns_list = ["none"]

        df.drop(skip_columns_list, axis=1, inplace=True)

        data_set = df.to_csv(header=True, index=False)

    if req_file.name.endswith('.csv'):
        data_set = req_file.read().decode('UTF-8')

    if not (req_file.name.endswith('.csv') or req_file.name.endswith('.xls') or req_file.name.endswith('.xlsx')):
        messages.error(request, req_file.name + ' : THIS IS NOT A XLS/XLSX/CSV FILE.')
        return HttpResponseRedirect(reverse("imf-list"))

    # delete existing records
    print('Deleted existing BrokerIcidirMf data')
    BrokerIcidirMf.objects.all().filter(bim_user_id=request.user.id).delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    # skip top 1 row
    next(io_string)

    skip_records = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
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
    return HttpResponseRedirect(reverse("imf-list"))
