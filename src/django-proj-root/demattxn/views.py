from django.shortcuts import render

# Create your views here.

from demattxn.models import DematTxn

from django.utils import timezone

from django.views.generic.list import ListView

from django.db.models import DateTimeField, DateField, F, ExpressionWrapper, fields, Max, Min
from django.db.models.functions import Trunc, ExtractDay
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

    # now = timezone.now()
    date_now = datetime.today().strftime('%Y-%m-%d')
    # time_diff = ExpressionWrapper(date_now - F('txn_date'), output_field=fields.DurationField())
    # time_diff = ExpressionWrapper(F('due_date'')-Now())
    # ,min_txn_date = Min('txn_date')
    # days=ExpressionWrapper(date_now - F('txn_date'), output_field=fields.DurationField())
    queryset = DematTxn.objects.values('stock_symbol').annotate(max_txn_date=Max('txn_date')).order_by('max_txn_date')

    # annotate(time_diff=time_diff).order_by('time_diff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
