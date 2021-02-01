# Create your views here.
from django.views.generic.list import ListView

from django.urls import reverse
from django.http import HttpResponseRedirect

import urllib.request
import csv
import io
from datetime import date, timedelta
import pandas as pd

from django_gotolong.trendlyne.models import Trendlyne


class TrendlyneListView(ListView):
    model = Trendlyne
    queryset = Trendlyne.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TrendlyneRecoView(ListView):
    model = Trendlyne
    queryset = Trendlyne.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# one parameter named request
def trendlyne_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "trendlyne/trendlyne_list.html"
    data = Trendlyne.objects.all()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)

    # delete existing records
    print('Deleted existing Trendlyne data')
    Trendlyne.objects.all().delete()

    # req_file = request.FILES['file']
    for req_file in request.FILES.getlist("files"):

        # let's check if it is a csv file
        print(req_file)

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
            columns_list = ['tl_stock_name', 'tl_isin', 'tl_bat', 'tl_der', 'tl_roce3',
                            'tl_roe3', 'tl_dpr2', 'tl_sales2', 'tl_profit5', 'tl_icr',
                            'tl_pledge', 'tl_low_3y', 'tl_low_5y']
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
            return HttpResponseRedirect(reverse("trendlyne-list"))

        # setup a stream which is when we loop through each line we are able to handle a data in a stream

        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimiter=',', quotechar='"'):
            tl_stock_name = column[0].strip()
            tl_isin = column[1].strip()
            tl_bat = column[2].strip()
            tl_der = column[3].strip()
            tl_roce3 = column[4].strip()
            tl_roe3 = column[5].strip()
            tl_dpr2 = column[6].strip()
            tl_sales2 = column[7].strip()
            tl_profit5 = column[8].strip()
            tl_icr = column[9].strip()
            tl_pledge = column[10].strip()
            tl_low_3y = column[11].strip()
            tl_low_5y = column[12].strip()

            # this should be handled somehow
            if tl_der == '-':
                # not sure what to do with it
                tl_der = 0.432

            # this should be handled somehow
            if tl_roce3 == '-':
                # not sure what to do with it
                tl_roce3 = 0.432

            # this should be handled somehow
            if tl_roe3 == '-':
                # not sure what to do with it
                tl_roe3 = 0.432

            # this should be handled somehow
            if tl_dpr2 == '-':
                # not sure what to do with it
                tl_dpr2 = 0.432

            # this should be handled somehow
            if tl_sales2 == '-':
                # not sure what to do with it
                tl_sales2 = 0.432

            # this should be handled somehow
            if tl_profit5 == '-':
                # not sure what to do with it
                tl_profit5 = 0.432

            # this should be handled somehow
            if tl_icr == '-':
                # not sure what to do with it
                tl_icr = 0.432

            # this should be handled somehow
            if tl_pledge == '-':
                # not sure what to do with it
                tl_pledge = 0.432

            print(tl_stock_name)

            _, created = Trendlyne.objects.update_or_create(
                tl_stock_name=tl_stock_name,
                tl_isin=tl_isin,
                tl_bat=tl_bat,
                tl_der=tl_der,
                tl_roce3=tl_roce3,
                tl_roe3=tl_roe3,
                tl_dpr2=tl_dpr2,
                tl_sales2=tl_sales2,
                tl_profit5=tl_profit5,
                tl_icr=tl_icr,
                tl_pledge=tl_pledge,
                tl_low_3y=tl_low_3y,
                tl_low_5y=tl_low_5y
            )
    # context = {}
    # render(request, template, context)
    print('Completed loading new Trendlyne data')
    return HttpResponseRedirect(reverse("trendlyne-list"))

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
