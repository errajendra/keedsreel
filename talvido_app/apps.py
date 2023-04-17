from django.apps import AppConfig


class TalvidoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'talvido_app'

    def ready(self):
        import talvido_app.signals
