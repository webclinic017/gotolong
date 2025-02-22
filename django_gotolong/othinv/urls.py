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

from django_gotolong.othinv.views import OthinvListView, OthinvListView_AssetType
from django_gotolong.othinv.views import Othinv_update, Othinv_add

urlpatterns = [
    path('list/', OthinvListView.as_view(), name='othinv-list'),
    path('update/<id>/', Othinv_update, name='othinv-update'),
    path('add/', Othinv_add, name='othinv-add'),
    path('asset-type/list/', OthinvListView_AssetType.as_view(), name='othinv-asset-type-list'),
]
