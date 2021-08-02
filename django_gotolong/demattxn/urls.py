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

from django_gotolong.demattxn.views import DematTxnListView, DematTxnGapView, DematTxnStatView, \
    DematTxnStatBuySellView, DematTxnRefreshView

from django_gotolong.demattxn.views import DematTxnYearArchiveView, DematTxnMonthArchiveView

urlpatterns = [
    path('list/', DematTxnListView.as_view(), name='demattxn-list'),
    path('gap/', DematTxnGapView.as_view(), name='demattxn-gap-list'),
    path('refresh/', DematTxnRefreshView.as_view(), name='demattxn-refresh'),
    path('stat/', DematTxnStatView.as_view(), name='demattxn-stat-list'),
    path('stat/buy_sell/', DematTxnStatBuySellView.as_view(),
         name='demattxn-stat-buysell-list'),
    path('list/<str:year>/', DematTxnYearArchiveView.as_view(),
         name='demattxn_archive_year'),
    path('list/<int:year>/<int:month>/',
         DematTxnMonthArchiveView.as_view(month_format='%m'),
         name='demattxn_archive_month_numeric'),
    path('list/<int:year>/<str:month>/', DematTxnMonthArchiveView.as_view(),
         name='demattxn_archive_month')
]
