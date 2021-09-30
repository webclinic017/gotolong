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

from django_gotolong.mfund.views import MfundListView, \
    MfundListView_Category, MfundListView_Amount, MfundListView_Subcat, \
    MfundListView_AMC, MfundListView_AMC_Amount, MfundListView_SubcatAmount, \
    MfundListView_Reco, Mfund_upload, Mfund_fetch

urlpatterns = [
    path('list/', MfundListView.as_view(), name='mfund-list'),
    path('amc/list/', MfundListView_AMC.as_view(), name='mfund-list-amc'),
    path('amc/amount/list/', MfundListView_AMC_Amount.as_view(), name='mfund-list-amc'),
    path('category/list/', MfundListView_Category.as_view(), name='mfund-list-category'),
    path('amount/list/', MfundListView_Amount.as_view(), name='mfund-list-amount'),
    path('subcat/list/', MfundListView_Subcat.as_view(), name='mfund-list-subcat'),
    path('subcat/amount/list/', MfundListView_SubcatAmount.as_view(), name='mfund-list-subcat-amount'),
    path('reco/list/', MfundListView_Reco.as_view(), name='mfund-list-reco'),
    path('fetch/', Mfund_fetch, name='mfund-fetch'),
    path('upload/', Mfund_upload, name='mfund-upload'),
]
