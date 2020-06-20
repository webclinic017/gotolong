from django.shortcuts import render

# Create your views here.

from .models import Dividend

from django.utils import timezone
from django.views.generic.list import ListView

from dividend.models import Dividend


class DividendListView(ListView):
    model = Dividend
    # if pagination is desired
    # paginate_by = 300

    queryset = Dividend.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
