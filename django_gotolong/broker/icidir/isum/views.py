# Create your views here.

from .models import BrokerIcidirSum

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.list import ListView

from django.db.models import OuterRef, Subquery, Count, Sum
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


class BrokerIcidirSumListView(ListView):
    model = BrokerIcidirSum

    # if pagination is desired
    # paginate_by = 300

    queryset = BrokerIcidirSum.objects.all()

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

    debug_level = 1
    # declaring template
    # only POST method is supported with upload
    # avoid direct access to this url
    template = "invalid-get-request.html"
    data = BrokerIcidirSum.objects.all()

    # GET request returns the value of the data with the specified key.
    print("method : ", request.method, template)
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
        if sheet_name != 'Data':
            print("sheet name changed to", sheet_name)

        # ignore top two line : Average Market Capitalization of listed companies during the six months ended
        # remove top two line from dataframe
        df = df.iloc[2:]

        if debug_level > 0:
            print("old columns : ")
            print(df.columns)

        # change column name of data frame
        columns_list = ['bis_stock_symbol', 'bis_company_name', 'bis_isin_code_id', 'bis_qty', 'bis_acp',
                        'bis_cmp', 'bis_pct_change', 'bis_value_cost', 'bis_value_market',
                        'bis_days_gain', 'bis_days_gain_pct', 'bis_realized_pl', 'bis_unrealized_pl',
                        'bis_unrealized_pl_pct', 'bis_unused1']
        df.columns = columns_list

        if debug_level > 0:
            print("new columns : ")
            print(df.columns)

        # Keep only top 1000 entries
        df = df.iloc[:1000]

        # round avg_mcap
        # df = df.round({'avg_mcap' : 1})
        # covert to numeric
        # df[["avg_mcap"]] = df[["avg_mcap"]].apply(pd.to_numeric)
        df[["avg_mcap"]] = df[["avg_mcap"]].astype(int)

        # drop columns that are not required
        # skip_columns_list = ['bse_mcap', 'nse_mcap', 'mse_symbol', 'mse_mcap']
        # df.drop(skip_columns_list, axis=1, inplace=True)

        data_set = df.to_csv(header=True, index=False)

    if req_file.name.endswith('.csv'):
        data_set = req_file.read().decode('UTF-8')

    if not (req_file.name.endswith('.csv') or req_file.name.endswith('.xls') or req_file.name.endswith('.xlsx')):
        messages.error(request, req_file.name + ' : THIS IS NOT A XLS/XLSX/CSV FILE.')
        return HttpResponseRedirect(reverse("broker-icidir-sum-list"))

    # delete existing records
    print('Deleted existing BrokerIcidirSum data')
    BrokerIcidirSum.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        column[0] = column[0].strip()
        column[1] = column[1].strip()

        _, created = BrokerIcidirSum.objects.update_or_create(
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
    # context = {}
    # render(request, template, context)
    lastrefd_update("broker-icidir-sum")
    #
    print('Completed loading new BrokerIcidirSum data')
    return HttpResponseRedirect(reverse("broker-icidir-sum-list"))
