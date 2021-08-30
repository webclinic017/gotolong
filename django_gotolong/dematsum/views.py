# Create your views here.

from .models import DematSum

from django.conf import settings
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.list import ListView
from django.views import View

from django.db.models import OuterRef, Subquery, Count, Sum, Max, Min
from django.db.models.functions import Trim, Lower, Round

from django_gotolong.amfi.models import Amfi
from django_gotolong.gfundareco.models import Gfundareco

import pandas as pd
import csv, io
import openpyxl
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_gotolong.lastrefd.models import Lastrefd, lastrefd_update

from django_gotolong.broker.icidir.isum.models import BrokerIcidirSum

class DematSumListView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # queryset = DematSum.objects.all()

    def get_queryset(self):
        return DematSum.objects.all().filter(ds_user_id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DematSumListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_amount = (DematSum.objects.all().filter(ds_user_id=self.request.user.id). \
                        aggregate(mktvalue=Sum('ds_mktvalue')))['mktvalue']
        if total_amount:
            total_amount = round(total_amount)
        context["total_amount"] = total_amount
        return context

class DematSumTickerView(ListView):
    model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # select required columns instead of all columns
    queryset = DematSum.objects.values('ds_ticker')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematSumRankView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("ds_isin"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        values('ds_ticker', 'ds_costvalue', 'comp_rank', 'cap_type'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumRecoView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("ds_isin"))
    gfunda_reco_qs = Gfundareco.objects.filter(funda_reco_isin=OuterRef("ds_isin"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        annotate(funda_reco_type=Subquery(gfunda_reco_qs.values('funda_reco_type')[:1])). \
        annotate(funda_reco_cause=Subquery(gfunda_reco_qs.values('funda_reco_cause')[:1])). \
        values('ds_ticker', 'ds_costvalue', 'comp_rank', 'cap_type', 'funda_reco_type',
               'funda_reco_cause'). \
        order_by('comp_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumAmountView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    queryset = DematSum.objects.all(). \
        values('ds_ticker', 'ds_costvalue'). \
        order_by('-ds_costvalue')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DematSumCapTypeView(ListView):
    # model = DematSum

    # if pagination is desired
    # paginate_by = 300

    # amfi_qset = Amfi.objects.filter(comp_isin=OuterRef('pk'))
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank'))).order_by('comp_rank')
    # queryset = DematSum.objects.annotate(comp_rank=Subquery(amfi_qset.values('comp_rank')))
    amfi_qs = Amfi.objects.filter(comp_isin=OuterRef("ds_isin"))
    queryset = DematSum.objects.all(). \
        annotate(comp_rank=Subquery(amfi_qs.values('comp_rank')[:1])). \
        annotate(cap_type=Lower(Trim(Subquery(amfi_qs.values('cap_type')[:1])))). \
        values('cap_type'). \
        annotate(cap_count=Count('cap_type')). \
        annotate(cap_cost=Round(Sum('ds_costvalue'))). \
        order_by('cap_type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DematSumRefreshView(View):
    fr_buy = {}
    fr_hold = {}
    fr_enabled = {}
    isin_industry_dict = {}
    debug_level = 1

    def get(self, request):
        self.dematsum_refresh(request)
        return HttpResponseRedirect(reverse("dematsum-list"))

    def __init__(self):
        super(DematSumRefreshView, self).__init__()

    def dematsum_refresh(self, request):
        debug_level = 1
        # declaring template
        template = "gfundareco/gfunda_reco_list.html"

        # first delete all existing dematsum objects
        DematSum.objects.all().filter(ds_user_id=request.user.id).delete()
        max_id_instances = DematSum.objects.aggregate(max_id=Max('ds_id'))
        max_ds_id = max_id_instances['max_id']
        print('DS: found max id ', max_ds_id)
        if max_ds_id is None:
            max_ds_id = 0
            print('max_ds_id ', max_ds_id)

        unique_id = max_ds_id
        for brec in BrokerIcidirSum.objects.all().filter(bis_user_id=request.user.id):
            unique_id += 1
            print(brec.bis_stock_symbol, brec.bis_isin_code_id, brec.bis_qty)
            print(brec.bis_acp, brec.bis_value_cost, brec.bis_value_market)
            _, created = DematSum.objects.update_or_create(
                ds_id=unique_id,
                ds_user_id=request.user.id,
                ds_broker='icidir',
                ds_ticker=brec.bis_stock_symbol,
                ds_isin=brec.bis_isin_code_id,
                ds_qty=brec.bis_qty,
                ds_acp=brec.bis_acp,
                ds_costvalue=brec.bis_value_cost,
                ds_mktvalue=brec.bis_value_market
            )

        # breakpoint()

        # import pdb
        # pdb.set_trace()

        # Updated Gfundareco objects
        lastrefd_update("dematsum")
