from django.apps import AppConfig


class HomeConfig(AppConfig):
    def ready(self):
        import home.signals.cache   # noqa
