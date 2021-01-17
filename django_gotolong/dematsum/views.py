# Create your views here.

from .models import DematSum

from django.views.generic.list import ListView

from django.db.models import OuterRef, Subquery, Count, Sum
from django.db.models.functions import Trim, Lower, Round

from django_gotolong.amfi.models import Amfi
from django_gotolong.greco.models import Greco

import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


class DematSumListView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    queryset = DematSum.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematSumTickerView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # select required columns instead of all columns
    queryset = DematSum.objects.values('stock_symbol')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematSumRankView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("isin_code_id"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        values('stock_symbol', 'comp_name', 'value_cost', 'comp_rank', 'cap_type'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumRecoView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("isin_code_id"))
    greco_qs = Greco.objects.filter(reco_isin=OuterRef("isin_code_id"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
        values('stock_symbol', 'comp_name', 'value_cost', 'comp_rank', 'cap_type', 'reco_type',
               'reco_cause'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumAmountView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    queryset = DematSum.objects.all(). \
        values('comp_name', 'value_cost'). \
        order_by('-value_cost')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumCapTypeView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("isin_code_id"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        values('cap_type'). \
        annotate(cap_count=Count('cap_type')). \
        annotate(cap_cost=Round(Sum('value_cost'))). \
        order_by('cap_type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# one parameter named request
def dematsum_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "dematsum/dematsum_list.html"
    data = DematSum.objects.all()

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
        if sheet_name != 'Data':
            print("sheet name changed to", sheet_name)

        # ignore top two line : Average Market Capitalization of listed companies during the six months ended
        # remove top two line from dataframe
        df = df.iloc[2:]

        if debug_level > 0:
            print("old columns : ")
            print(df.columns)

        # change column name of data frame
        columns_list = ['stock_symbol', 'comp_name', 'isin_code_id', 'qty', 'acp',
                        'cmp', 'pct_change', 'value_cost', 'value_market',
                        'days_gain', 'days_gain_pct', 'realized_pl', 'unrealized_pl',
                        'unrealized_pl_pct', 'unused1']
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
        return HttpResponseRedirect(reverse("dematsum-list"))

    # delete existing records
    print('Deleted existing DematSum data')
    DematSum.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        column[0] = column[0].strip()
        column[1] = column[1].strip()

        _, created = DematSum.objects.update_or_create(
            stock_symbol=column[0],
            comp_name=column[1],
            isin_code_id=column[2],
            qty=column[3],
            acp=column[4],
            cmp=column[5],
            pct_change=column[6],
            value_cost=column[7],
            value_market=column[8],
            days_gain=column[9],
            days_gain_pct=column[10],
            realized_pl=column[11],
            unrealized_pl=column[12],
            unrealized_pl_pct=column[13],
            unused1=column[14]
        )
    # context = {}
    # render(request, template, context)
    print('Completed loading new Dematsum data')
    return HttpResponseRedirect(reverse("dematsum-list"))

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
