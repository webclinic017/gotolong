# Create your views here.

from django_gotolong.demattxn.models import DematTxn

from django.utils import timezone

from django.views import View
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

from django_gotolong.broker.icidir.txn.models import BrokerIcidirTxn

class DematTxnYearArchiveView(YearArchiveView):
    queryset = DematTxn.objects.all()
    date_field = "dt_date"
    make_object_list = True
    allow_future = True

    year_list = DematTxn.objects.dates('dt_date', 'year')
    month_list = DematTxn.objects.dates('dt_date', 'month')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_list"] = self.year_list
        context["month_list"] = self.month_list
        txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())
        total_amount = round(DematTxn.objects.all().filter(dt_date__year=self.get_year()).
                             aggregate(txn_amount=Sum(txn_amount))['txn_amount'])

        summary_list = (
            DematTxn.objects.all().filter(dt_date__year=self.get_year()).
                annotate(
                month=ExtractMonth('dt_date')).values('month').annotate(
                Total=Round(Sum(txn_amount)))).order_by('month')
        context["total_amount"] = total_amount
        context["summary_list"] = summary_list
        return context


class DematTxnMonthArchiveView(MonthArchiveView):
    queryset = DematTxn.objects.all()
    date_field = "dt_date"
    make_object_list = True
    allow_future = True


class DematTxnListView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300
    queryset = DematTxn.objects.all()

    year_list = DematTxn.objects.dates('dt_date', 'year')

    # month_list = DematTxn.objects.dates('dt_date', 'month')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_list"] = self.year_list
        #  context["month_list"] = self.month_list
        txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())
        total_amount = round(DematTxn.objects.all().aggregate(txn_amount=Sum(txn_amount))[
                                 'txn_amount'])
        summary_list = (
            DematTxn.objects.all().annotate(
                year=ExtractYear('dt_date')).values('year').annotate(
                Total=Round(Sum(txn_amount)))).order_by('year')
        context["total_amount"] = total_amount
        context["summary_list"] = summary_list
        return context


class DematTxnGapView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300
    date_now = timezone.now()
    # date_now = datetime.today().strftime('%Y-%m-%d')
    time_diff = ExpressionWrapper(- F('dt_date'), output_field=fields.DurationField())
    # time_diff = ExpressionWrapper(F('due_date'')-Now())
    # ,min_dt_date = Min('dt_date')
    # days=ExpressionWrapper(date_now - F('dt_date'), output_field=fields.DurationField())
    # date_fmt = '%Y-%m-%d'
    # annotate(dt_date_fmt=RawSQL('DATE_FORMAT(dt_date, "%Y-%m-%d")',())).\
    # annotate(str_datetime=Cast('dt_date', CharField())). \
    #         annotate(str_datetime=Cast('dt_date', CharField())). \

    queryset = DematTxn.objects. \
        values('dt_ticker'). \
        annotate(max_dt_date=Max('dt_date')). \
        order_by('max_dt_date'). \
        annotate(months_gap=Min(RawSQL('TIMESTAMPDIFF(month, dt_date, curdate())', ()))). \
        order_by('-months_gap')

    # annotate(first_time_diff=RawSQL('TIMESTAMPDIFF(month, dt_date, curdate())', ())). \
    # annotate(time_diff=Max('first_time_diff')).\
    # annotate(max_dt_date=Cast('dt_date', CharField())).\
    # order_by('time_diff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DematTxnStatView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300
    txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())
    queryset = DematTxn.objects.all(). \
        annotate(txn_year=ExtractYear('dt_date')). \
        values('txn_year').annotate(txn_amount=Round(Sum(txn_amount))). \
        order_by('txn_year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematTxnStatBuySellView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300
    txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())
    queryset = DematTxn.objects.all(). \
        annotate(txn_year=ExtractYear('dt_date')). \
        values('txn_year', 'dt_action').annotate(txn_amount=Round(Sum(txn_amount))). \
        order_by('txn_year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def dt_date_iso(self, dt_date):
    month_name_abbr_to_num_dict = {name: num for num, name in enumerate(calendar.month_abbr) if num}

    try:
        # dd-mmm-yy
        dt_date_arr = dt_date.split('-')
        txn_day = dt_date_arr[0].strip()
        txn_month = dt_date_arr[1].strip()
        txn_year = dt_date_arr[2].strip()
        if txn_month.isdigit():
            # get rid of leading 0 in month number
            txn_month = str(int(txn_month))
        else:
            # month name to number
            txn_month = str(month_name_abbr_to_num_dict[txn_month])
        dt_date_iso = txn_year + "-" + txn_month + "-" + txn_day
        # ignore rest
    except ValueError:
        logging.error('ValueError ', dt_date, row_list)
    except IndexError:
        logging.error('IndexError ', dt_date, row_list)

    return dt_date_iso


class DematTxnRefreshView(View):
    debug_level = 1

    def get(self, request):
        self.demattxn_refresh(request)
        return HttpResponseRedirect(reverse("demattxn-list"))

    def __init__(self):
        super(DematTxnRefreshView, self).__init__()

    def demattxn_refresh(self, request):
        debug_level = 1
        # declaring template
        template = "gfundareco/gfunda_reco_list.html"

        # first delete all existing dematsum objects
        DematTxn.objects.all().delete()

        unique_id = 1
        for brec in BrokerIcidirTxn.objects.all():
            print(brec.stock_symbol, brec.isin_code, brec.quantity)
            print(brec.txn_price, brec.txn_date)
            _, created = DematTxn.objects.update_or_create(
                dt_id=unique_id,
                dt_broker='icidir',
                dt_ticker=brec.stock_symbol,
                dt_isin=brec.isin_code,
                dt_quantity=brec.quantity,
                dt_price=brec.txn_price,
                dt_amount=(brec.quantity * brec.txn_price),
                dt_date=brec.txn_date
            )
            unique_id += 1

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # Updated Gfundareco objects
        lastrefd_update("demattxn")

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
