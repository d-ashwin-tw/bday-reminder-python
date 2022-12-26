from django.apps import AppConfig


class AuthManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth_manager'

    def ready(self):
        import apps.auth_manager.signals