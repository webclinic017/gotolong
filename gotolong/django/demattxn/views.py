from django.shortcuts import render

# Create your views here.

from demattxn.models import DematTxn

from django.utils import timezone

from django.views.generic.list import ListView

from django.db.models import DateField, IntegerField, F, ExpressionWrapper, fields, Max, Min, Sum, CharField
from django.db.models.functions import ExtractYear, Round, Trunc, ExtractDay, Cast, TruncSecond, TruncDay
from django.db.models.expressions import RawSQL

from django.db.models.expressions import Func

from datetime import datetime


class DematTxnListView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300

    queryset = DematTxn.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematTxnGapView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300
    date_now = timezone.now()
    # date_now = datetime.today().strftime('%Y-%m-%d')
    time_diff = ExpressionWrapper(- F('txn_date'), output_field=fields.DurationField())
    # time_diff = ExpressionWrapper(F('due_date'')-Now())
    # ,min_txn_date = Min('txn_date')
    # days=ExpressionWrapper(date_now - F('txn_date'), output_field=fields.DurationField())
    # date_fmt = '%Y-%m-%d'
    # annotate(txn_date_fmt=RawSQL('DATE_FORMAT(txn_date, "%Y-%m-%d")',())).\
    # annotate(str_datetime=Cast('txn_date', CharField())). \
    #         annotate(str_datetime=Cast('txn_date', CharField())). \

    queryset = DematTxn.objects. \
        values('stock_symbol'). \
        annotate(max_txn_date=Max('txn_date')). \
        order_by('max_txn_date'). \
        annotate(months_gap=Min(RawSQL('TIMESTAMPDIFF(month, txn_date, curdate())', ()))). \
        order_by('-months_gap')

    # annotate(first_time_diff=RawSQL('TIMESTAMPDIFF(month, txn_date, curdate())', ())). \
    # annotate(time_diff=Max('first_time_diff')).\
    # annotate(max_txn_date=Cast('txn_date', CharField())).\
    # order_by('time_diff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematTxnStatView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300
    txn_amount = ExpressionWrapper(F('quantity') * F('txn_price'), output_field=IntegerField())
    queryset = DematTxn.objects.all(). \
        annotate(txn_year=ExtractYear('txn_date')). \
        values('txn_year').annotate(txn_amount=Round(Sum(txn_amount))). \
        order_by('txn_year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematTxnStatBuySellView(ListView):
    model = DematTxn

    # if pagination is desired
    # paginate_by = 300
    txn_amount = ExpressionWrapper(F('quantity') * F('txn_price'), output_field=IntegerField())
    queryset = DematTxn.objects.all(). \
        annotate(txn_year=ExtractYear('txn_date')). \
        values('txn_year', 'action').annotate(txn_amount=Round(Sum(txn_amount))). \
        order_by('txn_year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
