from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView

from trendlyne.models import Trendlyne

from django.db.models import CharField, Value, Q

from django.conf import settings


class TrendlyneListView(ListView):
    model = Trendlyne
    queryset = Trendlyne.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TrendlyneRecoView(ListView):
    model = Trendlyne

    b_c1 = Q(der__lte=settings.GL_CONFIG_DER_BUY)
    b_c2 = Q(roce3__gte=settings.GL_CONFIG_ROCE3_BUY)
    b_c3 = Q(dpr2__gte=settings.GL_CONFIG_DPR2_BUY)
    b_c4 = Q(sales2__gte=settings.GL_CONFIG_SALES2_BUY)
    b_c5 = Q(profit5__gte=settings.GL_CONFIG_PROFIT5_BUY)
    b_c6 = Q(pledge__lte=settings.GL_CONFIG_PLEDGE_BUY)

    queryset_buy = Trendlyne.objects.all(). \
        filter(b_c1 and b_c2 and b_c3 and b_c4 and b_c5 and b_c6). \
        annotate(reco_type=Value('BUY', CharField()))

    s_c1 = Q(der__gt=settings.GL_CONFIG_DER_HOLD)
    s_c2 = Q(roce3__lt=settings.GL_CONFIG_ROCE3_HOLD)
    s_c3 = Q(dpr2__lt=settings.GL_CONFIG_DPR2_HOLD)
    s_c4 = Q(sales2__lt=settings.GL_CONFIG_SALES2_HOLD)
    s_c5 = Q(profit5__lt=settings.GL_CONFIG_PROFIT5_HOLD)
    s_c6 = Q(pledge__gt=settings.GL_CONFIG_PLEDGE_HOLD)
    queryset_sale = Trendlyne.objects.all(). \
        filter(s_c1 or s_c2 or s_c3 or s_c4 or s_c5 or s_c6). \
        annotate(reco_type=Value('SALE', CharField()))

    queryset = queryset_buy.union(queryset_sale)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
