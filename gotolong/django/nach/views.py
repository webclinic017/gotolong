from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from .models import Nach

from django.utils import timezone
from django.views.generic.list import ListView

# from django_filters.rest_framework import DjangoFilterBackend, FilterSet, OrderingFilter


from nach.models import Nach


class NachListView(ListView):
    model = Nach
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Nach.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
