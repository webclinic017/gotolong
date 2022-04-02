# Create your views here.
from django.views.generic.list import ListView

from django_gotolong.fratio.models import Fratio
from django_gotolong.fratio.forms import FratioForm

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.template.context_processors import csrf


class FratioListView(ListView):
    model = Fratio
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFratio,]
    # ordering_fields = ['sno', 'nse_symbol']
    queryset = Fratio.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def Fratio_update(request, id):
    inst = get_object_or_404(Fratio, pk=id)
    if request.method == 'POST':  # If the form has been submitted...
        form = FratioForm(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("fratio-list"))
    else:
        form = FratioForm(instance=inst)  # A bound form
        action = inst.get_update_url()
        c = {'form': form, 'id': id, 'action': action}
        c.update(csrf(request))
        # desupported - render_to_response
        # return render_to_reponse('add_update.html', c)
        return render(request, 'add_update.html', c)


def Fratio_add(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = FratioForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("fratio-list"))
        else:
            raise RuntimeError('Form is invalid')
    else:
        form = FratioForm()  # An unbound form
        action = Fratio().get_add_url()
        c = {'form': form, 'action': action}
        c.update(csrf(request))
        return render(request, 'add_update.html', c)
