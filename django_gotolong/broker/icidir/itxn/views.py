# Create your views here.

from django_gotolong.broker.icidir.itxn.models import BrokerIcidirTxn

from django.utils import timezone

from django.views.generic.list import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView

from django.db.models import IntegerField, F, ExpressionWrapper, fields, Max, Min, Sum, Count
from django.db.models.functions import (ExtractYear, Round, ExtractMonth)
from django.db.models.expressions import RawSQL

import calendar
import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.comm import comfun

class BrokerIcidirTxnListView(ListView):
    model = BrokerIcidirTxn

    # if pagination is desired
    # paginate_by = 300
    # queryset = BrokerIcidirTxn.objects.all()
    # month_list = BrokerIcidirTxn.objects.dates('txn_date', 'month')

    def get_queryset(self):
        return BrokerIcidirTxn.objects.all().filter(bit_user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def txn_date_iso(self, txn_date):
    month_name_abbr_to_num_dict = {name: num for num, name in enumerate(calendar.month_abbr) if num}

    try:
        # dd-mmm-yy
        txn_date_arr = txn_date.split('-')
        txn_day = txn_date_arr[0].strip()
        txn_month = txn_date_arr[1].strip()
        txn_year = txn_date_arr[2].strip()
        if txn_month.isdigit():
            # get rid of leading 0 in month number
            txn_month = str(int(txn_month))
        else:
            # month name to number
            txn_month = str(month_name_abbr_to_num_dict[txn_month])
        txn_date_iso = txn_year + "-" + txn_month + "-" + txn_day
        # ignore rest
    except ValueError:
        logging.error('ValueError ', txn_date, row_list)
    except IndexError:
        logging.error('IndexError ', txn_date, row_list)

    return txn_date_iso


# one parameter named request
def BrokerIcidirTxnUpload(request):
    # for quick debugging
    #
    # import pdb; pdb.set_trace()
    #
    # breakpoint()

    template = "invalid-get-request.html"
    # change column name of data frame
    columns_list = ['bit_stock_symbol', 'bit_company_name', 'bit_isin_code', 'bit_action', 'bit_quantity',
                    'bit_txn_price', 'bit_brokerage', 'bit_txn_charges', 'bit_stamp_duty',
                    'bit_segment', 'bit_stt', 'bit_remarks', 'bit_txn_date',
                    'bit_exchange', 'bit_unused1']
    list_url_name = "broker-icidir-txn-list"
    data_set = comfun.comm_func_upload(request, template, columns_list, list_url_name)

    # delete existing records
    print('Deleted existing BrokerIcidirTxn data')
    BrokerIcidirTxn.objects.all().filter(bit_user_id=request.user.id).delete()
    max_id_instances = BrokerIcidirTxn.objects.aggregate(max_id=Max('bit_id'))
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

        # convert dd-mmm-yy to YYYY-mm-dd
        txn_date = txn_date_iso(request, column[12])

        print(unique_id, column)

        _, created = BrokerIcidirTxn.objects.update_or_create(
            bit_id=unique_id,
            bit_user_id=request.user.id,
            bit_stock_symbol=column[0],
            bit_company_name=column[1],
            bit_isin_code=column[2],
            bit_action=column[3],
            bit_quantity=column[4],
            bit_txn_price=column[5],
            bit_brokerage=column[6],
            bit_txn_charges=column[7],
            bit_stamp_duty=column[8],
            bit_segment=column[9],
            bit_stt=column[10],
            bit_remarks=column[11],
            bit_txn_date=txn_date,
            bit_exchange=column[13],
            bit_unused1=column[14]
        )

    lastrefd_update("broker-icidir-txn")

    print('Completed loading new BrokerIcidirTxn data')
    return HttpResponseRedirect(reverse(list_url_name))
