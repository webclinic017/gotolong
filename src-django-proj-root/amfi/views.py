from django.shortcuts import render

# Create your views here.

from .models import Amfi

from django.utils import timezone
from django.views.generic.list import ListView

# from django_filters.rest_framework import DjangoFilterBackend, FilterSet, OrderingFilter

from django.db.models import OuterRef, Subquery
from django.db.models import IntegerField, ExpressionWrapper, F

from amfi.models import Amfi

from dematsum.models import DematSum
from weight.models import Weight

class AmfiListView(ListView):
    model = Amfi
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Amfi.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AmfiAmountView(ListView):
    dematsum_qs = DematSum.objects.filter(isin_code=OuterRef("comp_isin"))
    weight_qs = Weight.objects.filter(cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(value_cost=Subquery(dematsum_qs.values('value_cost')[:1])). \
        annotate(cap_weight=Subquery(weight_qs.values('cap_weight')[:1])). \
        annotate(deficit=ExpressionWrapper(F('cap_weight') * 1000 - F('value_cost'), output_field=IntegerField())). \
        values('comp_rank', 'comp_name', 'value_cost', 'deficit'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class AmfiDeficitView(ListView):
    dematsum_qs = DematSum.objects.filter(isin_code=OuterRef("comp_isin"))
    weight_qs = Weight.objects.filter(cap_type=OuterRef("cap_type"))
    queryset = Amfi.objects.all(). \
        annotate(value_cost=Subquery(dematsum_qs.values('value_cost')[:1])). \
        annotate(cap_weight=Subquery(weight_qs.values('cap_weight')[:1])). \
        annotate(deficit=ExpressionWrapper(F('cap_weight') * 1000 - F('value_cost'), output_field=IntegerField())). \
        values('comp_rank', 'comp_name', 'value_cost', 'deficit'). \
        filter(value_cost__isnull=False). \
        order_by('-deficit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class AmfiMissingView(ListView):
    dematsum_qs = DematSum.objects.filter(isin_code=OuterRef("comp_isin"))
    weight_qs = Weight.objects.filter(cap_type=OuterRef("cap_type"))
    # missing large cap and mid cap : top 250 only
    queryset = Amfi.objects.all(). \
        annotate(value_cost=Subquery(dematsum_qs.values('value_cost')[:1])). \
        annotate(cap_weight=Subquery(weight_qs.values('cap_weight')[:1])). \
        annotate(deficit=ExpressionWrapper(F('cap_weight') * 1000 - F('value_cost'), output_field=IntegerField())). \
        values('comp_rank', 'comp_name', 'value_cost', 'deficit'). \
        filter(value_cost__isnull=True).filter(comp_rank__lte=250).order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
