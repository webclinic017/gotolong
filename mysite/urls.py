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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

from django_gotolong.amfi.views import AmfiListView, AmfiAmountView, AmfiDeficitView, AmfiMissingView, amfi_upload

from django_gotolong.bhav.views import BhavListView, bhav_fetch, bhav_upload
from django_gotolong.bstmtdiv.views import BstmtDivListView, bstmtdiv_upload
from django_gotolong.bstmtdiv.views import BstmtDivYearArchiveView, BstmtDivMonthArchiveView, BstmtDivAmountView, \
    BstmtDivFrequencyView

from django_gotolong.corpact.views import CorpactListView, corpact_upload

from django_gotolong.dbstat.views import DbstatListView

from django_gotolong.dematsum.views import DematSumListView, DematSumRankView, DematSumTickerView, DematSumAmountView, \
    DematSumCapTypeView, DematSumRecoView, dematsum_upload
from django_gotolong.demattxn.views import DematTxnListView, DematTxnGapView, DematTxnStatView, \
    DematTxnStatBuySellView, demattxn_upload

from django_gotolong.dividend.views import DividendListView, DividendRefreshView, DividendTickerListView

from django_gotolong.ftwhl.views import FtwhlListView, ftwhl_fetch, ftwhl_upload
from django_gotolong.fratio.views import FratioListView
from django_gotolong.greco.views import GrecoListView, GrecoRefreshView
from django_gotolong.gweight.views import GweightListView

from django_gotolong.indices.views import IndicesListView, IndicesIndustryView
from django_gotolong.indices.views import Indices_fetch, Indices_upload

from django_gotolong.lastrefd.views import LastrefdListView
from django_gotolong.nach.views import NachListView
from django_gotolong.phealth.views import PhealthListView_All, PhealthListView_Buy
from django_gotolong.phealth.views import PhealthListView_Sell, PhealthListView_Hold
from django_gotolong.trendlyne.views import TrendlyneListView, TrendlyneRecoView, trendlyne_upload

from django_gotolong.uploaddoc import views

from django_gotolong.jsched.tasks import jsched_task_startup

urlpatterns = [
                  path('', PhealthListView_All.as_view(), name='index'),
                  path('admin/', admin.site.urls),
                  path('amfi/list/', AmfiListView.as_view(), name='amfi-list'),
                  path('amfi/upload/', amfi_upload, name='amfi-upload'),
                  path('amfi/amount/', AmfiAmountView.as_view(), name='amfi-amount-list'),
                  path('amfi/deficit/', AmfiDeficitView.as_view(), name='amfi-deficit-list'),
                  path('amfi/missing/', AmfiMissingView.as_view(), name='amfi-missing-list'),
                  path('bhav/list/', BhavListView.as_view(), name='bhav-list'),
                  path('bhav/fetch/', bhav_fetch, name='bhav-fetch'),
                  path('bhav/upload/', bhav_upload, name='bhav-upload'),
                  path('bstmtdiv/list/', BstmtDivListView.as_view(), name='bstmtdiv-list'),
                  path('bstmtdiv/list/<str:year>/', BstmtDivYearArchiveView.as_view(),
                       name='bstmtdiv_archive_year'),
                  path('bstmtdiv/list/<int:year>/<int:month>/',
                       BstmtDivMonthArchiveView.as_view(month_format='%m'),
                       name='bstmtdiv_archive_month_numeric'),
                  path('bstmtdiv/list/<int:year>/<str:month>/', BstmtDivMonthArchiveView.as_view(),
                       name='bstmtdiv_archive_month'),
                  path('bstmtdiv/amount/', BstmtDivAmountView.as_view(),
                       name='bstmtdiv-amount-list'),
                  path('bstmtdiv/frequency/', BstmtDivFrequencyView.as_view(),
                       name='bstmtdiv-frequency-list'),
                  path('bstmtdiv/upload/', bstmtdiv_upload, name='bstmt-upload'),
                  path('bhav/fetch/', bhav_fetch, name='bhav-fetch'),
                  path('corpact/list/', CorpactListView.as_view(), name='corpact-list'),
                  path('corpact/upload/', corpact_upload, name='corpact-upload'),
                  path('dbstat/list/', DbstatListView.as_view(), name='dbstat-list'),
                  path('demat/sum/list/', DematSumListView.as_view(), name='dematsum-list'),
                  path('demat/sum/upload/', dematsum_upload, name='dematsum-upload'),
                  path('demat/sum/ticker/', DematSumTickerView.as_view(), name='dematsum-ticker-list'),
                  path('demat/sum/rank/', DematSumRankView.as_view(), name='dematsum-rank-list'),
                  path('demat/sum/amount/', DematSumAmountView.as_view(), name='dematsum-amount-list'),
                  path('demat/sum/captype/', DematSumCapTypeView.as_view(), name='dematsum-rank-list'),
                  path('demat/sum/reco/', DematSumRecoView.as_view(), name='dematsum-reco-list'),
                  path('demat/txn/list/', DematTxnListView.as_view(), name='demattxn-list'),
                  path('demat/txn/gap/', DematTxnGapView.as_view(), name='demattxn-gap-list'),
                  path('demat/txn/stat/', DematTxnStatView.as_view(), name='demattxn-stat-list'),
                  path('demat/txn/stat/buy_sell/', DematTxnStatBuySellView.as_view(),
                       name='demattxn-stat-buysell-list'),
                  path('demat/txn/upload/', demattxn_upload, name='demattxn-upload'),
                  path('dividend/list/', DividendListView.as_view(), name='dividend-list'),
                  path('dividend/refresh/', DividendRefreshView.as_view(), name='dividend-refresh'),
                  path('dividend/ticker/', DividendTickerListView.as_view(),
                       name='dividend-ticker-list'),
                  path('fratio/list/', FratioListView.as_view(), name='fratio-list'),
                  path('ftwhl/list/', FtwhlListView.as_view(), name='ftwhl-list'),
                  path('ftwhl/fetch/', ftwhl_fetch, name='ftwhl-fetch'),
                  path('ftwhl/upload/', ftwhl_upload, name='ftwhl-upload'),
                  path('greco/list/', GrecoListView.as_view(), name='greco-list'),
                  path('greco/refresh/', GrecoRefreshView.as_view(), name='greco-refresh'),
                  path('gweight/list/', GweightListView.as_view(), name='gweight-list'),
                  path('indices/list/', IndicesListView.as_view(), name='indices-list'),
                  path('indices/industry/', IndicesIndustryView.as_view(), name='indices-industry-list'),
                  path('indices/fetch/', Indices_fetch, name='indices-fetch'),
                  path('indices/upload/', Indices_upload, name='indices-upload'),
                  path('lastrefd/list/', LastrefdListView.as_view(), name='lastrefd-list'),
                  path('nach/list/', NachListView.as_view(), name='nach-list'),
                  path('page/about/', TemplateView.as_view(template_name="about.html")),
                  path('page/contact/', TemplateView.as_view(template_name="contact.html")),
                  path('page/global-data/', TemplateView.as_view(template_name="global_data.html")),
                  path('page/quick-links/', TemplateView.as_view(template_name="quick_links.html")),
                  path('page/sitemap/', TemplateView.as_view(template_name="sitemap.html")),
                  path('page/user-data/', TemplateView.as_view(template_name="user_data.html")),
                  path('phealth/list/all/', PhealthListView_All.as_view(), name='phealth-list-all'),
                  path('phealth/list/buy/', PhealthListView_Buy.as_view(), name='phealth-list-buy'),
                  path('phealth/list/hold/', PhealthListView_Hold.as_view(), name='phealth-list-hold'),
                  path('phealth/list/sell/', PhealthListView_Sell.as_view(), name='phealth-list-sell'),
                  path('trendlyne/list/', TrendlyneListView.as_view(), name='trendlyne-list'),
                  path('trendlyne/reco/', TrendlyneRecoView.as_view(), name='trendlyne-reco-list'),
                  path('trendlyne/upload/', trendlyne_upload, name='trendlyne-upload'),
                  path('uploaddoc/simple/', views.simple_upload, name='uploaddoc-simple'),
                  path('uploaddoc/model-form/', views.model_form_upload, name='uploaddoc-model-form'),
                  path('uploaddoc/list/', views.list, name='uploaddoc-list'),
                  path('uploaddoc/delete/<int:id>/', views.delete_view, name='uploaddoc-delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

jsched_task_startup()
