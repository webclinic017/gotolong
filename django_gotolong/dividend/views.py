# Create your views here.

# To address, NameError: name 'Sum' is not defined
from django.db.models import Sum

from django.db.models.functions import (ExtractYear, Round, ExtractMonth)
from django.db.models import (Count)

from django.views.generic.list import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView

from django_gotolong.dividend.models import Dividend


class DividendYearArchiveView(YearArchiveView):
    queryset = Dividend.objects.all()
    date_field = "div_date"
    make_object_list = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_amount = round(
            Dividend.objects.all().filter(div_date__year=self.get_year()).aggregate(Sum('amount'))['amount__sum'])
        summary_list = (
            Dividend.objects.all().filter(div_date__year=self.get_year()).annotate(
                month=ExtractMonth('div_date')).values('month').annotate(
                Total=Round(Sum('amount'))))
        context["total_amount"] = total_amount
        context["summary_list"] = summary_list
        return context


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
    month_list = Dividend.objects.dates('div_date', 'month')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_list"] = self.year_list
        context["month_list"] = self.month_list
        # aggregate returns dictionary
        # get value from dictionary
        total_amount = round(Dividend.objects.all().aggregate(Sum('amount'))[
                                 'amount__sum'])
        summary_list = (
            Dividend.objects.all().annotate(
                year=ExtractYear('div_date')).values('year').annotate(
                Total=Round(Sum('amount'))))
        month_summary_list = (
            Dividend.objects.all().annotate(
                month=ExtractMonth('div_date')).values('month').annotate(
                Total=Round(Sum('amount')))).order_by('month')
        context["total_amount"] = total_amount
        context["summary_list"] = summary_list
        context["month_summary_list"] = month_summary_list
        return context


class DividendAmountView(ListView):
    model = Dividend
    # if pagination is desired
    # paginate_by = 300
    queryset = Dividend.objects.all()

    year_list = Dividend.objects.dates('div_date', 'year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_list"] = self.year_list
        # aggregate returns dictionary
        # get value from dictionary
        summary_list = (
            Dividend.objects.all().values('ticker')
                .annotate(Total=Round(Sum('amount')))).order_by('-Total')
        context["summary_list"] = summary_list
        return context


class DividendFrequencyView(ListView):
    model = Dividend
    # if pagination is desired
    # paginate_by = 300
    queryset = Dividend.objects.all()

    year_list = Dividend.objects.dates('div_date', 'year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year_list"] = self.year_list
        # aggregate returns dictionary
        # get value from dictionary
        summary_list = (
            Dividend.objects.all().values('ticker')
                .annotate(Total=Round(Count('ticker')))).order_by('-Total')
        context["summary_list"] = summary_list
        return context
