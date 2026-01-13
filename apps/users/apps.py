from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'  # <--- IMPORTANTE: debe coincidir con INSTALLED_APPS
