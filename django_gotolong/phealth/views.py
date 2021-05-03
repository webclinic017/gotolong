# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.amfi.models import Amfi

from django_gotolong.bhav.models import Bhav

from django_gotolong.corpact.models import Corpact

from django_gotolong.dematsum.models import DematSum
from django_gotolong.demattxn.models import DematTxn

from django_gotolong.ftwhl.models import Ftwhl

from django_gotolong.greco.models import Greco
from django_gotolong.gweight.models import Gweight

from django_gotolong.trendlyne.models import Trendlyne

from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, IntegerField, Count

from django_gotolong.jsched.tasks import jsched_task_bg, jsched_task_daily
from django.utils import timezone


# from django_gotolong.ftwhl.views import ftwhl_fetch

class PhealthListView_All(ListView):
    # crete task
    # jsched_task_bg(schedule=timezone.now())
    jsched_task_daily()
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
    ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
    ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
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
        annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
        annotate(txn_date=Subquery(demattxn_qs.values('txn_date')[:1])). \
        annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
        annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
        annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                 output_field=IntegerField())). \
        annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                              output_field=IntegerField())). \
        filter(cur_oku__isnull=False). \
        filter(bat__isnull=False). \
        values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low', 'safety_margin', 'low_margin',
               'ca_total', 'txn_date', 'plan_oku', 'cur_oku', 'tbd_oku', 'reco_type', 'reco_cause'). \
        order_by('-safety_margin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reco_list = (Greco.objects.all().values('reco_type').annotate(reco_count=Count('reco_type')).
                     order_by('reco_count'))

        context["reco_list"] = reco_list

        return context

    def get_template_names(self):
        app_label = 'phealth'
        template_name_first = app_label + '/' + 'phealth_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class PhealthListView_Buy(ListView):
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
    ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
    ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
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
        annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
        annotate(txn_date=Subquery(demattxn_qs.values('txn_date')[:1])). \
        annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
        annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
        annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                 output_field=IntegerField())). \
        annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                              output_field=IntegerField())). \
        filter(cur_oku__isnull=False). \
        filter(bat__isnull=False). \
        filter(reco_type='Buy'). \
        values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low', 'safety_margin', 'low_margin',
               'ca_total', 'txn_date', 'plan_oku', 'cur_oku', 'tbd_oku', 'reco_type', 'reco_cause'). \
        order_by('low_margin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reco_list = (Greco.objects.all().values('reco_type').annotate(reco_count=Count('reco_type')).
                     order_by('reco_count'))

        context["reco_list"] = reco_list

        return context

    def get_template_names(self):
        app_label = 'phealth'
        template_name_first = app_label + '/' + 'phealth_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class PhealthListView_Sell(ListView):
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
    ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
    ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
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
        annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
        annotate(txn_date=Subquery(demattxn_qs.values('txn_date')[:1])). \
        annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
        annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
        annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                 output_field=IntegerField())). \
        annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                              output_field=IntegerField())). \
        filter(cur_oku__isnull=False). \
        filter(reco_type='Sell'). \
        values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low', 'safety_margin', 'low_margin',
               'ca_total', 'txn_date', 'plan_oku', 'cur_oku', 'tbd_oku', 'reco_type', 'reco_cause'). \
        order_by('safety_margin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reco_list = (Greco.objects.all().values('reco_type').annotate(reco_count=Count('reco_type')).
                     order_by('reco_count'))

        context["reco_list"] = reco_list

        return context

    def get_template_names(self):
        app_label = 'phealth'
        template_name_first = app_label + '/' + 'phealth_list.html'
        template_names_list = [template_name_first]
        return template_names_list

class PhealthListView_Hold(ListView):
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    bhav_qs = Bhav.objects.filter(bhav_isin=OuterRef("comp_isin"))
    ca_qs = Corpact.objects.filter(ca_ticker=OuterRef("nse_symbol"))
    ftwhl_qs = Ftwhl.objects.filter(ftwhl_ticker=OuterRef("nse_symbol"))
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
        annotate(ca_total=Subquery(ca_qs.values('ca_total')[:1])). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
        annotate(txn_date=Subquery(demattxn_qs.values('txn_date')[:1])). \
        annotate(bhav_price=Subquery(bhav_qs.values('bhav_price')[:1])). \
        annotate(ftwhl_low=Subquery(ftwhl_qs.values('ftwhl_low')[:1])). \
        annotate(safety_margin=ExpressionWrapper((F('bat') - F('bhav_price')) * 100.0 / F('bhav_price'),
                                                 output_field=IntegerField())). \
        annotate(low_margin=ExpressionWrapper((F('bhav_price') - F('ftwhl_low')) * 100.0 / F('ftwhl_low'),
                                              output_field=IntegerField())). \
        filter(cur_oku__isnull=False). \
        filter(reco_type='Hold'). \
        values('nse_symbol', 'comp_name', 'bhav_price', 'bat', 'ftwhl_low', 'safety_margin', 'low_margin',
               'ca_total', 'txn_date', 'plan_oku', 'cur_oku', 'tbd_oku', 'reco_type', 'reco_cause'). \
        order_by('-safety_margin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reco_list = (Greco.objects.all().values('reco_type').annotate(reco_count=Count('reco_type')).
                     order_by('reco_count'))

        context["reco_list"] = reco_list

        return context

    def get_template_names(self):
        app_label = 'phealth'
        template_name_first = app_label + '/' + 'phealth_list.html'
        template_names_list = [template_name_first]
        return template_names_list
