# Create your views here.

from django.views.generic.list import ListView

from django_gotolong.amfi.models import Amfi
from django_gotolong.bhav.models import Bhav
from django_gotolong.bstmtdiv.models import BstmtDiv
from django_gotolong.corpact.models import Corpact
from django_gotolong.dematsum.models import DematSum
from django_gotolong.demattxn.models import DematTxn
from django_gotolong.dividend.models import Dividend
from django_gotolong.fratio.models import Fratio
from django_gotolong.ftwhl.models import Ftwhl
from django_gotolong.gfundareco.models import Gfundareco
from django_gotolong.gweight.models import Gweight
from django_gotolong.indices.models import Indices
from django_gotolong.lastrefd.models import Lastrefd
# from django_gotolong.screener.models import Screener
from django_gotolong.trendlyne.models import Trendlyne
from django_gotolong.fofeti.models import Fofeti
from django_gotolong.mfund.models import Mfund

from django_gotolong.broker.icidir.isum.models import BrokerIcidirSum
from django_gotolong.broker.icidir.itxn.models import BrokerIcidirTxn
from django_gotolong.broker.icidir.imf.models import BrokerIcidirMf


class DbstatListView(ListView):
    # model = Phealth
    # if pagination is desired
    # paginate_by = 300
    # filter_backends = [filters.OrderingFilter,]
    # ordering_fields = ['sno', 'nse_symbol']
    db_stat = {}

    db_stat['amfi'] = Amfi.objects.count()
    db_stat['bim'] = BrokerIcidirMf.objects.count()
    db_stat['bis'] = BrokerIcidirSum.objects.count()
    db_stat['bit'] = BrokerIcidirTxn.objects.count()
    db_stat['bhav'] = Bhav.objects.count()
    db_stat['bstmtdiv'] = BstmtDiv.objects.count()
    db_stat['corpact'] = Corpact.objects.count()
    db_stat['dematsum'] = DematSum.objects.count()
    db_stat['demattxn'] = DematTxn.objects.count()
    db_stat['dividend'] = Dividend.objects.count()
    db_stat['fratio'] = Fratio.objects.count()
    db_stat['ftwhl'] = Ftwhl.objects.count()
    db_stat['gfundareco'] = Gfundareco.objects.count()
    db_stat['gweight'] = Gweight.objects.count()
    db_stat['fofeti'] = Fofeti.objects.count()
    db_stat['indices'] = Indices.objects.count()
    db_stat['lastrefd'] = Lastrefd.objects.count()
    db_stat['mfund'] = Mfund.objects.count()
    # db_stat['screener'] = Screener.objects.count()
    db_stat['trendlyne'] = Trendlyne.objects.count()

    db_rows = 0

    queryset = Amfi.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["db_stat"] = self.db_stat

        for k in self.db_stat.keys():
            v = self.db_stat[k]
            print(k, v)
            self.db_rows += v
        print('total rows', self.db_rows)

        context["db_rows"] = self.db_rows

        return context

    def get_template_names(self):
        app_label = 'dbstat'
        template_name_first = app_label + '/' + 'dbstat_list.html'
        template_names_list = [template_name_first]
        return template_names_list
