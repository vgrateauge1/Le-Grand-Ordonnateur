from django.apps import AppConfig


class PlmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'
    
    def ready(self):
        import backend.signal  # Importez les signaux ici
