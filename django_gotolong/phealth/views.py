# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.amfi.models import Amfi
from django_gotolong.dematsum.models import DematSum
from django_gotolong.demattxn.models import DematTxn
from django_gotolong.trendlyne.models import Trendlyne
from django_gotolong.gweight.models import Gweight

from django_gotolong.greco.models import Greco

from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, IntegerField


class PhealthListView(ListView):
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    greco_qs = Greco.objects.filter(reco_isin=OuterRef("comp_isin"))
    tl_qs = Trendlyne.objects.filter(tl_isin=OuterRef("comp_isin"))
    dematsum_qs = DematSum.objects.filter(isin_code=OuterRef("comp_isin"))
    demattxn_qs = DematTxn.objects.filter(isin_code=OuterRef("comp_isin")).order_by('-txn_date').values('txn_date')
    gweight_qs = Gweight.objects.filter(gw_cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(
        cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('value_cost')[:1]) / 1000, output_field=IntegerField())). \
        annotate(plan_oku=Subquery(gweight_qs.values('gw_cap_weight')[:1])). \
        annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
        annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
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
    greco_qs = Greco.objects.filter(reco_isin=OuterRef("comp_isin"))
    tl_qs = Trendlyne.objects.filter(tl_isin=OuterRef("comp_isin"))
    dematsum_qs = DematSum.objects.filter(isin_code=OuterRef("comp_isin"))
    demattxn_qs = DematTxn.objects.filter(isin_code=OuterRef("comp_isin")).order_by('-txn_date').values('txn_date')
    gweight_qs = Gweight.objects.filter(gw_cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(
        cur_oku=ExpressionWrapper(Subquery(dematsum_qs.values('value_cost')[:1]) / 1000, output_field=IntegerField())). \
        annotate(plan_oku=Subquery(gweight_qs.values('gw_cap_weight')[:1])). \
        annotate(tbd_oku=ExpressionWrapper(F('plan_oku') - F('cur_oku'), output_field=IntegerField())). \
        annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
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
