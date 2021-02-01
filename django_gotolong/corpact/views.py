# Create your views here.
from django.views.generic.list import ListView

from django.urls import reverse
from django.http import HttpResponseRedirect

import urllib.request
import csv
import io
from datetime import date, timedelta
import pandas as pd
import traceback
import re

from django_gotolong.corpact.models import Corpact


class CorpactListView(ListView):
    model = Corpact
    queryset = Corpact.objects.all().order_by('-ca_total')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CorpactRecoView(ListView):
    model = Corpact
    queryset = Corpact.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# one parameter named request
def corpact_upload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    debug_level = 1
    # declaring template
    template = "corpact/corpact_list.html"
    data = Corpact.objects.all()

    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)

    print('Deleted existing Corpact data for years: ')
    # delete existing records
    Corpact.objects.all().delete()

    # req_file = request.FILES['file']
    corp_act_stock_list = []
    corp_act_year_list = []

    corp_act_bonus_stock_year_dict = {}
    corp_act_buyback_stock_year_dict = {}
    corp_act_dividend_stock_year_dict = {}

    ca_score = {}

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
            return HttpResponseRedirect(reverse("corpact-list"))

        # setup a stream which is when we loop through each line we are able to handle a data in a stream

        io_string = io.StringIO(data_set)
        next(io_string)

        for row in csv.reader(io_string, delimiter=',', quotechar='"'):
            [security_code, security_name, company_name, ex_date, purpose,
             record_date, bc_state_date, bc_end_date, nd_start_date, nd_end_date,
             actual_payment_date] = row

            security_name = security_name.strip()
            purpose = purpose.strip()
            ex_date = ex_date.strip()

            if debug_level > 1:
                print(security_name)

            try:
                if purpose == '-' or purpose == 'Purpose':
                    continue

                if ex_date != 'Ex Date':
                    # sometime the space is separator and sometime hyphen is separator
                    if re.search('-', ex_date):
                        split_char = "-"
                    else:
                        split_char = " "
                    date_arr = ex_date.split(split_char)
                    if debug_level > 2:
                        print('date: ', date_arr)
                    current_year = int(date_arr[2])
                    # note: sometime date is stored as 17 and sometime as 2017
                    # to fix the year.
                    if current_year >= 2000:
                        current_year = current_year - 2000
                    if debug_level > 2:
                        print('year : ', current_year)

                    if security_name not in corp_act_stock_list:
                        corp_act_stock_list.append(security_name)
                    if current_year not in corp_act_year_list:
                        corp_act_year_list.append(current_year)

                    if re.search('Bonus', purpose):
                        if (security_name, current_year) not in corp_act_bonus_stock_year_dict:
                            corp_act_bonus_stock_year_dict[security_name, current_year] = 1
                    elif re.search('Buy Back', purpose):
                        if (security_name, current_year) not in corp_act_buyback_stock_year_dict:
                            corp_act_buyback_stock_year_dict[security_name, current_year] = 1
                    elif re.search('Dividend', purpose):
                        if (security_name, current_year) not in corp_act_dividend_stock_year_dict:
                            corp_act_dividend_stock_year_dict[security_name, current_year] = 1
                    else:
                        print('wrong purpose', purpose)

            except IndexError:
                print('IndexError', row)
                traceback.print_exc()
            except NameError:
                print('NameError', row)
                traceback.print_exc()
            except AttributeError:
                print('AttributeError', row)
                traceback.print_exc()

    print(corp_act_stock_list)
    print(corp_act_year_list)

    print(corp_act_bonus_stock_year_dict)
    print(corp_act_buyback_stock_year_dict)
    print(corp_act_dividend_stock_year_dict)

    for security_name in sorted(set(corp_act_stock_list)):
        buyback_found = 0
        bonus_found = 0
        dividend_found = 0

        for current_year in sorted(set(corp_act_year_list), key=int):
            try:
                if (security_name, current_year) in corp_act_buyback_stock_year_dict:
                    buyback_found += 1
                if (security_name, current_year) in corp_act_bonus_stock_year_dict:
                    bonus_found += 1
                if (security_name, current_year) in corp_act_dividend_stock_year_dict:
                    dividend_found += 1
                    if debug_level > 2:
                        print(security_name, current_year)

            except KeyError:
                print('KeyError failed lookup :', security_name, current_year)
        # do not include stock split as that doesn't mean giving back
        total_give_back = buyback_found + bonus_found + dividend_found
        ca_score[security_name, 'bonus'] = bonus_found
        ca_score[security_name, 'buyback'] = buyback_found
        ca_score[security_name, 'dividend'] = dividend_found
        ca_score[security_name, 'total'] = total_give_back

    for security_name in corp_act_stock_list:
        _, created = Corpact.objects.update_or_create(
            ca_ticker=security_name,
            ca_total=ca_score[security_name, 'total'],
            ca_bonus=ca_score[security_name, 'bonus'],
            ca_buyback=ca_score[security_name, 'buyback'],
            ca_dividend=ca_score[security_name, 'dividend']
        )
    # context = {}
    # render(request, template, context)
    print('Completed loading new Corpact data')
    return HttpResponseRedirect(reverse("corpact-list"))

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
