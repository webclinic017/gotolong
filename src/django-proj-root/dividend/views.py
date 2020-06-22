from django.shortcuts import render

# Create your views here.

from .models import Dividend

from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView

from dividend.models import Dividend


class DividendYearArchiveView(YearArchiveView):
    queryset = Dividend.objects.all()
    date_field = "div_date"
    make_object_list = True
    allow_future = True


class DividendMonthArchiveView(MonthArchiveView):
    queryset = Dividend.objects.all()
    date_field = "div_date"
    make_object_list = True
    allow_future = True

class DividendListView(ListView):
    model = Dividend
    # if pagination is desired
    # paginate_by = 300
    queryset = Dividend.objects.all()

    year_list = Dividend.objects.dates('div_date', 'year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_list"] = self.year_list
        return context
