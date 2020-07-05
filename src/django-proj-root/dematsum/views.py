from django.shortcuts import render

# Create your views here.

from .models import DematSum

from django.utils import timezone

from django.views.generic.list import ListView

from django.db.models import OuterRef, Subquery, Case, When, Value, IntegerField, CharField
from django.db.models.functions import Trim, Lower

from amfi.models import Amfi


class DematSumListView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    queryset = DematSum.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematSumTickerView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # select required columns instead of all columns
    queryset = DematSum.objects.values('stock_symbol')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DematSumRankView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("isin_code"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        values('stock_symbol', 'company_name', 'value_cost', 'comp_rank', 'cap_type'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context