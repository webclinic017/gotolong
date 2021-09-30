# Create your views here.

from .models import Mfund

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


class MfundListView(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Mfund.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context


class MfundListView_Amount(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Mfund.objects.all().exclude(mf_units=0.0).order_by('-mf_nav_value')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context


class MfundListView_AMC(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Mfund.objects.all().exclude(mf_units=0.0).order_by('mf_amc', 'mf_category', 'mf_subcat', '-mf_nav_value')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context


class MfundListView_AMC_Amount(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    queryset = Mfund.objects.all().exclude(mf_units=0.0).values('mf_amc').annotate(scheme_sum=Sum('mf_nav_value')). \
        exclude(scheme_sum=0.0).order_by('-scheme_sum')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = []
        values = []
        labels_values_dict = {}
        sum_total = 0
        for q_row in self.queryset:
            sum_total += q_row['scheme_sum']
            labels_values_dict[q_row['mf_amc']] = q_row['scheme_sum']
        context['sum_total'] = int(sum_total)

        print('labels values dict', labels_values_dict)

        for k, v in sorted(labels_values_dict.items(), key=lambda item: item[1]):
            labels.append(k)
            values.append(v)

        print('labels ', labels)
        print('values ', values)

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        # fig.show()

        plot_div_1 = plot(fig, output_type='div', include_plotlyjs=False)
        context['plot_div_1'] = plot_div_1

        return context


class MfundListView_Category(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Mfund.objects.all().exclude(mf_units=0.0).order_by('mf_category', 'mf_subcat', '-mf_nav_value')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context


class MfundListView_Subcat(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Mfund.objects.all().exclude(mf_units=0.0).order_by('mf_subcat', '-mf_nav_value')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context


class MfundListView_Reco(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Mfund.objects.all().exclude(mf_units=0.0).order_by('mf_research_reco', '-mf_rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Mfund_url()
        context["refresh_url"] = refresh_url
        return context


class MfundListView_SubcatAmount(ListView):
    model = Mfund
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    queryset = Mfund.objects.all().values('mf_subcat').annotate(scheme_sum=Sum('mf_nav_value')). \
        exclude(scheme_sum=0.0).order_by('-scheme_sum')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        labels = []
        values = []
        labels_values_dict = {}
        sum_total = 0
        for q_row in self.queryset:
            sum_total += q_row['scheme_sum']
            labels_values_dict[q_row['mf_subcat']] = q_row['scheme_sum']
        context['sum_total'] = int(sum_total)

        print('labels values dict', labels_values_dict)

        for k, v in sorted(labels_values_dict.items(), key=lambda item: item[1]):
            labels.append(k)
            values.append(v)

        print('labels ', labels)
        print('values ', values)

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        # fig.show()

        plot_div_1 = plot(fig, output_type='div', include_plotlyjs=False)
        context['plot_div_1'] = plot_div_1

        return context


def Mfund_url():
    url = 'https://archives.nseindia.com/content/mfund/ind_nifty500list.csv'

    return url


# one parameter named request
def Mfund_fetch(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()
    debug_level = 1
    print('fetch not supported')
    return HttpResponseRedirect(reverse("mfund-list"))


# one parameter named request
def Mfund_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "mfund/mfund_list.html"
    data = Mfund.objects.all()

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
        return HttpResponseRedirect(reverse("mfund-list"))

    # delete existing records
    print('Deleted existing Mfund data')
    Mfund.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    # skip top 1 row
    next(io_string)

    skip_records = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        mf_amc = column[0].strip()
        mf_name = column[1].strip()
        mf_category = column[2].strip()
        mf_subcat = column[3].strip()
        mf_rating = column[4].strip()
        mf_units = column[5].strip()
        mf_acp = column[6].strip()
        mf_cost_value = column[7].strip()
        mf_nav_date = column[8].strip()
        mf_nav = column[9].strip()
        mf_nav_value = column[10].strip()
        mf_pnl_realized = column[10].strip()
        mf_pnl = column[12].strip()
        mf_pnl_pct = column[13].strip()
        mf_research_reco = column[14].strip()

        # print('mf_units ', mf_units)
        # skip mutual funds with 0 holdings
        # if int(float(mf_units)) !=  0 :

        _, created = Mfund.objects.update_or_create(
            mf_amc=mf_amc,
            mf_name=mf_name,
            mf_category=mf_category,
            mf_subcat=mf_subcat,
            mf_rating=mf_rating,
            mf_units=mf_units,
            mf_acp=mf_acp,
            mf_cost_value=mf_cost_value,
            mf_nav_date=mf_nav_date,
            mf_nav=mf_nav,
            mf_nav_value=mf_nav_value,
            mf_pnl_realized=mf_pnl_realized,
            mf_pnl=mf_pnl,
            mf_pnl_pct=mf_pnl_pct,
            mf_research_reco=mf_research_reco
        )

    lastrefd_update("mfund")

    print('Skipped records', skip_records)
    print('Completed loading new Mfund data')
    return HttpResponseRedirect(reverse("mfund-list"))
