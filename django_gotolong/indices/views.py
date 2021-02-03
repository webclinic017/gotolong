# Create your views here.

from .models import Indices

from django.views.generic.list import ListView

from django.db.models import (Count)

from django.urls import reverse
from django.http import HttpResponseRedirect
import urllib3
import csv
import io

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update


class IndicesListView(ListView):
    model = Indices
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Indices.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refresh_url = Indices_url()
        context["refresh_url"] = refresh_url
        return context


class IndicesIndustryView(ListView):
    model = Indices
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    queryset = Indices.objects.all().values('ind_industry').annotate(comp_count=Count('ind_industry')). \
        order_by('-comp_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get count of Industries
        industries_count = len(Indices.objects.all().values('ind_industry'). \
                               annotate(industries_count=Count('ind_industry', distinct=True)))
        context['industries_count'] = industries_count
        return context


def Indices_url():
    url = 'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'

    return url


# one parameter named request
def Indices_fetch(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "indices/indices_list.html"
    data = Indices.objects.all()

    url = Indices_url()

    print(url)

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    print(response.status)

    if response.status == 200:
        print('delete existing indices data')
        Indices.objects.all().delete()

    resp_data = response.data

    # response data
    io_string = io.StringIO(resp_data.decode('utf-8'))
    # skip first three rows
    next(io_string)
    next(io_string)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        if debug_level > 1:
            print(column)

        ind_name = column[0].strip()
        ind_industry = column[1].strip()
        ind_ticker = column[2].strip()
        ind_series = column[3].strip()
        ind_isin = column[4].strip()

        _, created = Indices.objects.update_or_create(
            ind_name=ind_name,
            ind_industry=ind_industry,
            ind_ticker=ind_ticker,
            ind_isin=ind_isin
        )

    lastrefd_update("indices")
    return HttpResponseRedirect(reverse("indices-list"))


# one parameter named request
def Indices_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "indices/indices_list.html"
    data = Indices.objects.all()

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
        columns_list = ["NAME", "INDUSTRY", "SYMBOL", "SERIES", "ISIN"]
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
        df[["avg_mcap"]] = df[["avg_mcap"]].astype(int)

        # drop columns that are not required
        # skip_columns_list = ['bse_mcap', 'nse_mcap', 'mse_symbol', 'mse_mcap']
        # df.drop(skip_columns_list, axis=1, inplace=True)

        data_set = df.to_csv(header=True, index=False)

    if req_file.name.endswith('.csv'):
        data_set = req_file.read().decode('UTF-8')

    if not (req_file.name.endswith('.csv') or req_file.name.endswith('.xls') or req_file.name.endswith('.xlsx')):
        messages.error(request, req_file.name + ' : THIS IS NOT A XLS/XLSX/CSV FILE.')
        return HttpResponseRedirect(reverse("indices-list"))

    # delete existing records
    print('Deleted existing Indices data')
    Indices.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    # skip top three rows
    next(io_string)
    next(io_string)
    next(io_string)

    skip_records = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        ind_name = column[0].strip()
        ind_industry = column[1].strip()
        ind_ticker = column[2].strip()
        ind_series = column[3].strip()
        ind_isin = column[4].strip()

        _, created = Indices.objects.update_or_create(
            ind_name=ind_name,
            ind_industry=ind_industry,
            ind_ticker=ind_ticker,
            ind_isin=ind_isin
        )

    lastrefd_update("indices")

    print('Skipped records', skip_records)
    print('Completed loading new Indices data')
    return HttpResponseRedirect(reverse("indices-list"))
