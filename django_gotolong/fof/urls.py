"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django_gotolong.fof.views import FofListView, \
    Fof_upload, Fof_fetch
from django_gotolong.fof.views import FofIndustryView, \
    FofListView_Type, FofListView_Benchmark, FofListView_Benchmark_Select, \
    FofListView_AUM, FofListView_IMF, FofListView_NonGold_ETF, \
    FofListView_Gold_ETF, FofListView_Gold_MF

urlpatterns = [
    path('list/', FofListView.as_view(), name='fof-list'),
    path('list/aum/', FofListView_AUM.as_view(), name='fof-list-aum'),
    path('list/type/', FofListView_Type.as_view(), name='fof-list-type'),
    path('list/benchmark/', FofListView_Benchmark.as_view(), name='fof-list-benchmark'),
    path('list/benchmark-select/', FofListView_Benchmark_Select.as_view(), name='fof-list-benchmark-select'),
    path('list/index-mf/', FofListView_IMF.as_view(), name='fof-list-imf'),
    path('list/gold-etf/', FofListView_Gold_ETF.as_view(), name='fof-list-gold-etf'),
    path('list/gold-mf/', FofListView_Gold_MF.as_view(), name='fof-list-gold-mf'),
    path('list/non-gold-etf/', FofListView_NonGold_ETF.as_view(), name='fof-list-non-gold-etf'),
    path('industry/', FofIndustryView.as_view(), name='fof-industry-list'),
    path('fetch/', Fof_fetch, name='fof-fetch'),
    path('upload/', Fof_upload, name='fof-upload'),
]
