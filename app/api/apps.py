from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'app.api'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from drift import TuskDrift
        TuskDrift.get_instance().mark_app_as_ready()
