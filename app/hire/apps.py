from django.apps import AppConfig


class HireConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.hire'


    def ready(self):
        import app.hire.signals