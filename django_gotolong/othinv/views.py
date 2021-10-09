from django.views.generic.list import ListView

from django_gotolong.othinv.models import Othinv
from django_gotolong.othinv.forms import OthinvForm

from django.db.models import (Sum, Count)

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.template.context_processors import csrf

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class OthinvListView(ListView):
    model = Othinv

    def get_queryset(self):
        queryset = Othinv.objects.all().filter(othinv_user_id=self.request.user.id)
        return queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OthinvListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs2 = Othinv.objects.annotate(Sum('othinv_equity'))
        print('qs2 ', qs2);
        for qs2_item in qs2:
            print('qs2_item ', qs2_item)

        sum_total = 0
        sum_othinv_equity = (Othinv.objects.all().filter(othinv_user_id=self.request.user.id).
                             aggregate(sum_othinv_equity=Sum('othinv_equity')))['sum_othinv_equity']
        if sum_othinv_equity:
            sum_othinv_equity = round(sum_othinv_equity)
        else:
            sum_othinv_equity = 0
        sum_total += sum_othinv_equity
        context['sum_othinv_equity'] = sum_othinv_equity

        sum_othinv_debt = (Othinv.objects.all().filter(othinv_user_id=self.request.user.id).
                           aggregate(sum_othinv_debt=Sum('othinv_debt')))['sum_othinv_debt']
        if sum_othinv_debt:
            sum_othinv_debt = round(sum_othinv_debt)
        else:
            sum_othinv_debt = 0
        sum_total += sum_othinv_debt
        context['sum_othinv_debt'] = sum_othinv_debt

        sum_othinv_gold = (Othinv.objects.all().filter(othinv_user_id=self.request.user.id).
                           aggregate(sum_othinv_gold=Sum('othinv_gold')))['sum_othinv_gold']
        if sum_othinv_gold:
            sum_othinv_gold = round(sum_othinv_gold)
        else:
            sum_othinv_gold = 0

        sum_total += sum_othinv_gold
        context['sum_othinv_gold'] = sum_othinv_gold

        sum_othinv_intl = (Othinv.objects.all().filter(othinv_user_id=self.request.user.id).
                           aggregate(sum_othinv_intl=Sum('othinv_intl')))['sum_othinv_intl']

        if sum_othinv_intl:
            sum_othinv_intl = round(sum_othinv_intl)
        else:
            sum_othinv_intl = 0

        sum_total += sum_othinv_intl
        context['sum_othinv_intl'] = sum_othinv_intl

        sum_othinv_realty = (Othinv.objects.all().filter(othinv_user_id=self.request.user.id).
                             aggregate(sum_othinv_realty=Sum('othinv_realty')))['sum_othinv_realty']
        if sum_othinv_realty:
            sum_othinv_realty = round(sum_othinv_realty)
        else:
            sum_othinv_realty = 0

        sum_total += sum_othinv_realty
        context['sum_othinv_realty'] = sum_othinv_realty

        context['sum_total'] = sum_total
        return context


class OthinvListView_AssetType(ListView):
    model = Othinv

    def get_queryset(self):
        queryset = Othinv.objects.filter(othinv_user_id=self.request.user.id).annotate(Sum('othinv_equity'))
        for qs in queryset:
            print('qs ', qs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('queryset ', self.queryset)
        return context


def Othinv_update(request, id):
    inst = get_object_or_404(Othinv, pk=id)
    if request.method == 'POST':  # If the form has been submitted...
        form = OthinvForm(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("othinv-list"))
    else:
        form = OthinvForm(instance=inst)  # A bound form
        action = inst.get_update_url()
        c = {'form': form, 'id': id, 'action': action}
        c.update(csrf(request))
        # desupported - render_to_response
        # return render_to_reponse('add_update.html', c)
        return render(request, 'add_update.html', c)


def Othinv_add(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = OthinvForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("othinv-list"))
        else:
            raise RuntimeError('Form is invalid')
    else:
        form = OthinvForm()  # An unbound form
        action = Othinv().get_add_url()
        c = {'form': form, 'action': action}
        c.update(csrf(request))
        return render(request, 'add_update.html', c)
