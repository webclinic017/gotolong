from django.shortcuts import render

# Create your views here.

from django.views.generic.list import ListView

from amfi.models import Amfi
from dematsum.models import DematSum
from demattxn.models import DematTxn
from trendlyne.models import Trendlyne
from weight.models import Weight

from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, IntegerField, Min
from django.db.models.expressions import RawSQL


class PhealthListView(ListView):
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    tl_qs = Trendlyne.objects.filter(isin=OuterRef("comp_isin"))
    dematsum_qs = DematSum.objects.filter(isin_code=OuterRef("comp_isin"))
    demattxn_qs = DematTxn.objects.filter(isin_code=OuterRef("comp_isin")).order_by('-txn_date').values('txn_date')
    weight_qs = Weight.objects.filter(cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(
        cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('value_cost')[:1]) / 1000, output_field=IntegerField())). \
        annotate(plan_oku=Subquery(weight_qs.values('cap_weight')[:1])). \
        annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
        annotate(bat=Subquery(tl_qs.values('bat')[:1])). \
        annotate(reco_type=Subquery(tl_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(tl_qs.values('reco_cause')[:1])). \
        annotate(txn_date=Subquery(demattxn_qs.values('txn_date')[:1])). \
        filter(cur_oku__isnull=False). \
        filter(bat__isnull=False). \
        values('nse_symbol', 'comp_name', 'bat', 'txn_date', 'plan_oku', 'cur_oku', 'tbd_oku', 'reco_type',
               'reco_cause'). \
        order_by('-tbd_oku')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):
        app_label = 'phealth'
        template_name_first = app_label + '/' + 'phealth_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class PhealthListView_CSV(ListView):
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    tl_qs = Trendlyne.objects.filter(isin=OuterRef("comp_isin"))
    dematsum_qs = DematSum.objects.filter(isin_code=OuterRef("comp_isin"))
    demattxn_qs = DematTxn.objects.filter(isin_code=OuterRef("comp_isin")).order_by('-txn_date').values('txn_date')
    weight_qs = Weight.objects.filter(cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(
        cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('value_cost')[:1]) / 1000, output_field=IntegerField())). \
        annotate(plan_oku=Subquery(weight_qs.values('cap_weight')[:1])). \
        annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
        annotate(bat=Subquery(tl_qs.values('bat')[:1])). \
        annotate(reco_type=Subquery(tl_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(tl_qs.values('reco_cause')[:1])). \
        annotate(txn_date=Subquery(demattxn_qs.values('txn_date')[:1])). \
        filter(cur_oku__isnull=False). \
        filter(bat__isnull=False). \
        values('nse_symbol', 'comp_name', 'bat', 'txn_date', 'plan_oku', 'cur_oku', 'tbd_oku', 'reco_type',
               'reco_cause'). \
        order_by('-tbd_oku')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):
        app_label = 'phealth'
        template_name_first = app_label + '/' + 'phealth_list_csv.html'
        template_names_list = [template_name_first]
        return template_names_list
