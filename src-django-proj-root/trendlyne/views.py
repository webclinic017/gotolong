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
    queryset = Trendlyne.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context