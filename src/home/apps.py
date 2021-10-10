from django.apps import AppConfig


class HomeAppConfig(AppConfig):
    name = "home"

    def ready(self):
        import home.signals.cache  # noqa
        import home.signals.og_image  # noqa
