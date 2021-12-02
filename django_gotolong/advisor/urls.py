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

from django_gotolong.advisor.views import AdvisorListView_AllButNone, AdvisorListView_All, AdvisorListView_Buy
from django_gotolong.advisor.views import AdvisorListView_Sell, AdvisorListView_Hold, AdvisorListView_Insuf

urlpatterns = [
    path('list/all-none/', AdvisorListView_AllButNone.as_view(), name='advisor-list-all-but-none'),
    path('list/all/', AdvisorListView_All.as_view(), name='advisor-list-all'),
    path('list/buy/', AdvisorListView_Buy.as_view(), name='advisor-list-buy'),
    path('list/hold/', AdvisorListView_Hold.as_view(), name='advisor-list-hold'),
    path('list/sell/', AdvisorListView_Sell.as_view(), name='advisor-list-sell'),
    path('list/insuf/', AdvisorListView_Insuf.as_view(), name='advisor-list-insuf'),
]
