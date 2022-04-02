from django.apps import AppConfig

from django_gotolong.bhav.views import start

class BhavConfig(AppConfig):
    name = 'bhav'

    def ready(self):
        start()
