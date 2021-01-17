# Create your views here.
from django.views.generic.list import ListView

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
        columns_list = ['stock_symbol', 'comp_name', 'isin_code', 'action', 'quantity',
                        'txn_price', 'brokerage', 'txn_charges', 'stamp_duty',
                        'segment', 'stt', 'remarks', 'txn_date',
                        'exchange', 'unused1']
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

    # delete existing records
    print('Deleted existing Trendlyne data')
    Trendlyne.objects.all().delete()

    # setup a stream which is when we loop through each line we are able to handle a data in a stream

    io_string = io.StringIO(data_set)
    next(io_string)
    unique_id = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        unique_id += 1
        column[0] = column[0].strip()
        column[1] = column[1].strip()

        # convert dd-mmm-yy to YYYY-mm-dd
        txn_date = txn_date_iso(request, column[12])

        print(unique_id, column)

        _, created = Trendlyne.objects.update_or_create(
            dt_id=unique_id,
            stock_symbol=column[0],
            comp_name=column[1],
            isin_code=column[2],
            action=column[3],
            quantity=column[4],
            txn_price=column[5],
            brokerage=column[6],
            txn_charges=column[7],
            stamp_duty=column[8],
            segment=column[9],
            stt=column[10],
            remarks=column[11],
            txn_date=txn_date,
            exchange=column[13],
            unused1=column[14]
        )
    # context = {}
    # render(request, template, context)
    print('Completed loading new Trendlyne data')
    return HttpResponseRedirect(reverse("trendlyne-list"))

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
