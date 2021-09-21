# Create your views here.

from django_gotolong.demattxn.models import DematTxn

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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

from django_gotolong.broker.icidir.itxn.models import BrokerIcidirTxn

from plotly.offline import plot
import plotly.graph_objs as go


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
        total_amount = round(DematTxn.objects.all().filter(dt_user_id=self.request.user.id).
                             filter(dt_date__year=self.get_year()).
                             aggregate(txn_amount=Sum(txn_amount))['txn_amount'])

        summary_list = (
            DematTxn.objects.all().filter(dt_user_id=self.request.user.id).
                filter(dt_date__year=self.get_year()).
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
    # queryset = DematTxn.objects.all()

    year_list = DematTxn.objects.dates('dt_date', 'year')

    # month_list = DematTxn.objects.dates('dt_date', 'month')

    def get_queryset(self):
        return DematTxn.objects.all().filter(dt_user_id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DematTxnListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_list"] = self.year_list
        #  context["month_list"] = self.month_list
        txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())
        total_amount = (DematTxn.objects.all().filter(dt_user_id=self.request.user.id).
            aggregate(txn_amount=Sum(txn_amount))[
            'txn_amount'])
        if total_amount:
            total_amount = round(total_amount)
        summary_list = (
            DematTxn.objects.all().filter(dt_user_id=self.request.user.id).
                annotate(
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

    def get_queryset(self):
        return DematTxn.objects. \
            filter(dt_user_id=self.request.user.id). \
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

    def get_queryset(self):
        txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())

        return DematTxn.objects.all(). \
            filter(dt_user_id=self.request.user.id). \
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
    plot_div = ''

    def get_queryset(self):
        txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())
        queryset = DematTxn.objects.all(). \
            filter(dt_user_id=self.request.user.id). \
            annotate(txn_year=ExtractYear('dt_date')). \
            values('txn_year', 'dt_action').annotate(txn_amount=Round(Sum(txn_amount))). \
            order_by('txn_year')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        txn_amount = ExpressionWrapper(F('dt_quantity') * F('dt_price'), output_field=IntegerField())
        queryset = DematTxn.objects.all(). \
            filter(dt_user_id=self.request.user.id). \
            annotate(txn_year=ExtractYear('dt_date')). \
            values('txn_year', 'dt_action').annotate(txn_amount=Round(Sum(txn_amount))). \
            order_by('txn_year')

        buy_dict = {}
        sell_dict = {}
        year_list = []

        for q in queryset:
            # print('q ', q)
            for key in ['txn_year', 'dt_action']:
                if key == 'txn_year':
                    cur_year = q[key]
                    # print('year ', cur_year)
                    if q[key] not in year_list:
                        year_list.append(q[key])
                if key == 'dt_action':
                    if q[key] == 'Buy':
                        buy_dict[cur_year] = q['txn_amount']
                    else:
                        sell_dict[cur_year] = q['txn_amount']
                # print(key, q[key])

        min_year = min(year_list)
        max_year = max(year_list)
        # range skips top most element
        # added +1 to include data of latest year.
        year_list = list(range(min_year, max_year + 1))
        buy_list = []
        sell_list = []
        for cur_year in year_list:
            if cur_year in buy_dict:
                buy_list.append(buy_dict[cur_year])
            else:
                buy_list.append(0)
            if cur_year in sell_dict:
                sell_list.append(sell_dict[cur_year])
            else:
                sell_list.append(0)

        print(year_list)
        print(buy_list)
        print(sell_list)

        x_data = year_list
        y_data = buy_list
        if True:
            fig = go.Figure(data=[
                go.Bar(name='Buy', x=year_list, y=buy_list),
                go.Bar(name='Sell', x=year_list, y=sell_list)
            ])
            # Change the bar mode
            fig.update_layout(barmode='group')
            # plot_div = plot([fig],output_type='div', include_plotlyjs=False)
            plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        else:
            plot_div = plot([go.Scatter(x=x_data, y=y_data,
                                        mode='lines', name='test',
                                        opacity=0.8, marker_color='green')],
                            output_type='div', include_plotlyjs=False)

        context['plot_div'] = plot_div
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
        DematTxn.objects.all().filter(dt_user_id=self.request.user.id).delete()
        max_id_instances = DematTxn.objects.aggregate(max_id=Max('dt_id'))
        max_dt_id = max_id_instances['max_id']
        print('max_dt_id ', max_dt_id)
        if max_dt_id is None:
            max_dt_id = 0
            print('max_dt_id ', max_dt_id)

        unique_id = max_dt_id
        for brec in BrokerIcidirTxn.objects.all().filter(bit_user_id=request.user.id):
            unique_id += 1
            print(brec.bit_user_id, brec.bit_stock_symbol, brec.bit_isin_code)
            print(brec.bit_action, brec.bit_quantity)
            print(brec.bit_txn_price, brec.bit_txn_date)
            _, created = DematTxn.objects.update_or_create(
                dt_id=unique_id,
                dt_user_id=brec.bit_user_id,
                dt_broker='icidir',
                dt_ticker=brec.bit_stock_symbol,
                dt_isin=brec.bit_isin_code,
                dt_action=brec.bit_action,
                dt_quantity=brec.bit_quantity,
                dt_price=brec.bit_txn_price,
                dt_amount=(brec.bit_quantity * brec.bit_txn_price),
                dt_date=brec.bit_txn_date
            )

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # Updated Gfundareco objects
        lastrefd_update("demattxn")

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
