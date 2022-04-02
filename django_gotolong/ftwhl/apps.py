from django.apps import AppConfig

from django_gotolong.ftwhl.views import start

class FtwhlConfig(AppConfig):
    name = 'ftwhl'

    def ready(self):
        start()
