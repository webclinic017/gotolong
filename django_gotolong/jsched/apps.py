from django.apps import AppConfig


class JschedConfig(AppConfig):
    name = 'jsched'

    def ready(self):
        from django_gotolong.jsched.tasks import start

        print('JschedConfig - ready')
        start()
