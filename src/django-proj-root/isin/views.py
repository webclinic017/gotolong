from django.shortcuts import render

# Create your views here.

from .models import Isin

from django.utils import timezone
from django.views.generic.list import ListView

from django.db.models import (Count)

# from django_filters.rest_framework import DjangoFilterBackend, FilterSet, OrderingFilter

class IsinListView(ListView):
    model = Isin
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Isin.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IsinIndustryView(ListView):
    model = Isin
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']

    queryset = Isin.objects.all().values('comp_industry').annotate(comp_count=Count('comp_industry')). \
        order_by('-comp_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get count of Industries
        industries_count = len(Isin.objects.all().values('comp_industry'). \
                               annotate(industries_count=Count('comp_industry', distinct=True)))
        context['industries_count'] = industries_count
        return context

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
