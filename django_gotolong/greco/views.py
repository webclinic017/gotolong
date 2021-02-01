# Create your views here.

from django.views.generic.list import ListView

from django.http import HttpResponseRedirect
from django.views import View

from django.urls import reverse

from django_gotolong.amfi.models import Amfi
from django_gotolong.isin.models import Isin
from django_gotolong.fratio.models import Fratio
from django_gotolong.trendlyne.models import Trendlyne
from django_gotolong.gweight.models import Gweight
from django_gotolong.greco.models import Greco

from django.db.models import OuterRef, Subquery, ExpressionWrapper, F, IntegerField, Count


class GrecoListView(ListView):
    model = Greco
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Greco.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reco_list = (Greco.objects.all().values('reco_type').annotate(reco_count=Count('reco_type')).
                     order_by('reco_count'))

        context["reco_list"] = reco_list
        return context


class GrecoListView2(ListView):
    # model = Greco
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    tl_qs = Trendlyne.objects.filter(tl_isin=OuterRef("comp_isin"))
    gweight_qs = Gweight.objects.filter(gw_cap_type=OuterRef("cap_type"))
    greco_qs = Greco.objects.filter(reco_isin=OuterRef("comp_isin"))
    queryset = Amfi.objects.all(). \
        annotate(bat=Subquery(tl_qs.values('tl_bat')[:1])). \
        annotate(reco_type=Subquery(greco_qs.values('reco_type')[:1])). \
        annotate(reco_cause=Subquery(greco_qs.values('reco_cause')[:1])). \
        filter(bat__isnull=False). \
        values('nse_symbol', 'comp_name', 'bat', 'reco_type', 'reco_cause')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):
        app_label = 'greco'
        template_name_first = app_label + '/' + 'greco_list.html'
        template_names_list = [template_name_first]
        return template_names_list


class GrecoRefreshView(View):
    fr_buy = {}
    fr_hold = {}
    fr_enabled = {}
    isin_industry_dict = {}
    debug_level = 1

    def get(self, request):
        self.greco_refresh(request)
        return HttpResponseRedirect(reverse("greco-list"))

    def __init__(self):
        super(GrecoRefreshView, self).__init__()

    def greco_get_reco(self, stock_name, isin, bat, der, roce3,
                       roe3, dpr2, sales2, profit5, icr,
                       pledge, low_3y, low_5y, notes):

        ignore_der = False
        # skip debt for Financial Services like Bank/NBFC.
        if isin in self.isin_industry_dict:
            if self.debug_level > 1:
                print('tl', 'isin', isin, 'industry', self.isin_industry[isin])
            if self.isin_industry_dict[isin] == 'FINANCIAL SERVICES':
                ignore_der = True
        else:
            print(isin, 'not found in isin db')

        reco_type = 'NONE'
        reco_cause = ''

        if ignore_der:
            b_c1 = True
        else:
            b_c1 = der <= self.fr_buy['der']

        b_c2 = roce3 >= self.fr_buy['roce3']
        b_c3 = dpr2 >= self.fr_buy['dpr2']
        b_c4 = sales2 >= self.fr_buy['sales2']
        b_c5 = profit5 >= self.fr_buy['profit5']
        b_c6 = pledge <= self.fr_buy['pledge']

        # if isin == 'INE079A01024':
        #    breakpoint()

        if not b_c1:
            reco_cause += " "
            reco_cause = "-B(der)"
        if not b_c2:
            reco_cause += " "
            reco_cause = "-B(roce3)"
        if not b_c3:
            reco_cause += " "
            reco_cause = "-B(dpr2)"
        if not b_c4:
            reco_cause += " "
            reco_cause = "-B(sales)"
        if not b_c5:
            reco_cause += " "
            reco_cause = "-B(profit5)"
        if not b_c6:
            reco_cause += " "
            reco_cause = "-B(pledge)"

        if (b_c1 and b_c2 and b_c3 and b_c4 and b_c5 and b_c6):
            reco_type = "BUY"
            reco_cause = "ALL"
            return (reco_type, reco_cause)
        else:
            s_c1 = der > self.fr_hold['der']
            s_c2 = roce3 < self.fr_hold['roce3']
            s_c3 = dpr2 < self.fr_hold['dpr2']
            s_c4 = sales2 < self.fr_hold['sales2']
            s_c5 = profit5 < self.fr_hold['profit5']
            s_c6 = pledge > self.fr_hold['pledge']
            # avoid NONE
            reco_cause_buy = reco_cause
            reco_cause = ''

            if s_c1:
                if not ignore_der:
                    reco_cause += " "
                    reco_cause += "S(der)"
            if s_c2:
                reco_cause += " "
                reco_cause += "S(roce3)"
            if s_c3:
                reco_cause += " "
                reco_cause += "S(dpr2)"
            if s_c4:
                reco_cause += " "
                reco_cause += "S(sales2)"
            if s_c5:
                reco_cause += " "
                reco_cause += "S(profit5)"
            if s_c6:
                reco_cause += " "
                reco_cause += "S(pledge)"

            if reco_cause == '':
                reco_type = "HOLD"
            else:
                reco_type = "SALE"

        if reco_type == 'HOLD':
            h_c1 = (der > self.fr_buy['der'] and der <= self.fr_hold['der'])
            # fixed the bug here to get the cause for HOLD
            h_c2 = (roce3 < self.fr_buy['roce3'] and roce3 >= self.fr_hold['roce3'])
            h_c3 = (dpr2 < self.fr_buy['dpr2'] and dpr2 >= self.fr_hold['dpr2'])
            h_c4 = (sales2 < self.fr_buy['sales2'] and sales2 >= self.fr_hold['sales2'])
            h_c5 = (profit5 < self.fr_buy['profit5'] and profit5 >= self.fr_hold['profit5'])
            h_c6 = (pledge > self.fr_buy['pledge'] and pledge <= self.fr_hold['pledge'])

            if h_c1:
                if not ignore_der:
                    reco_cause += " "
                    reco_cause += "H(der)"
            if h_c2:
                reco_cause += " "
                reco_cause += "H(roce3)"
            if h_c3:
                reco_cause += " "
                reco_cause += "H(dpr2)"
            if h_c4:
                reco_cause += " "
                reco_cause += "H(sales2)"
            if h_c5:
                reco_cause += " "
                reco_cause += "H(profit5)"
            if h_c6:
                reco_cause += " "
                reco_cause += "H(pledge)"

            # for debugging
            if reco_cause == '':
                reco_cause = reco_cause_buy

        return (reco_type, reco_cause)

    def greco_refresh(self, request):
        debug_level = 1
        # declaring template
        template = "greco/greco_list.html"

        for fr in Fratio.objects.all():
            print(fr.fratio_name, fr.fratio_buy, fr.fratio_hold, fr.fratio_enabled)
            self.fr_buy[fr.fratio_name] = fr.fratio_buy
            self.fr_hold[fr.fratio_name] = fr.fratio_hold
            self.fr_enabled[fr.fratio_name] = fr.fratio_enabled

        for isin in Isin.objects.all():
            # strip unwanted new line
            isin.comp_isin = isin.comp_isin.rstrip()
            if debug_level > 1:
                print(isin.comp_isin, isin.comp_industry)
            self.isin_industry_dict[isin.comp_isin] = isin.comp_industry

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # first delete all existing greco objects
        Greco.objects.all().delete()

        for tl in Trendlyne.objects.all():

            # print(tl.stock_name, tl.isin)

            # using 0 for roe3
            # using notes itself as notes
            (reco_type, reco_cause) = \
                self.greco_get_reco(tl.tl_stock_name, tl.tl_isin, tl.tl_bat, tl.tl_der, tl.tl_roce3,
                                    tl.tl_roe3, tl.tl_dpr2, tl.tl_sales2, tl.tl_profit5, tl.tl_icr,
                                    tl.tl_pledge, tl.tl_low_3y, tl.tl_low_5y, "notes")

            if debug_level > 1:
                print(tl.tl_stock_name, tl.tl_isin, reco_type, reco_cause)

            # isin_obj = Isin.objects.get(comp_isin=tl.isin)
            # print(isin_obj.comp_ticker)

            # to avoid DoesNotExist exception
            amfi_obj = Amfi.objects.filter(comp_isin=tl.tl_isin).first()
            if amfi_obj:
                if debug_level > 1:
                    print(amfi_obj.nse_symbol)
                if tl.tl_isin == 'INE745G01035':
                    print('nse symbol', amfi_obj.nse_symbol)
                if amfi_obj.nse_symbol != '':
                    _, created = Greco.objects.update_or_create(
                        reco_ticker=amfi_obj.nse_symbol,
                        reco_isin=tl.tl_isin,
                        reco_type=reco_type,
                        reco_cause=reco_cause
                    )
            else:
                print('amfi obj failed for isin', tl.tl_isin, 'stock_name', tl.tl_stock_name)
        # context = {}
        # render(request, template, context)
