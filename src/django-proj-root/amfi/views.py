from django.shortcuts import render

# Create your views here.

from .models import Amfi

from django.utils import timezone
from django.views.generic.list import ListView

from amfi.models import Amfi


class AmfiListView(ListView):
    model = Amfi
    # if pagination is desired
    # paginate_by = 300

    queryset = Amfi.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# from django.http import HttpResponse
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")
#
