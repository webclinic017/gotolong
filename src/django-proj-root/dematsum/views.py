from django.shortcuts import render

# Create your views here.

from .models import DematSummary

from django.utils import timezone
from django.views.generic.list import ListView

from dematsum.models import DematSummary


class DematSummaryListView(ListView):
    model = DematSummary
    paginate_by = 300  # if pagination is desired

    queryset = DematSummary.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
