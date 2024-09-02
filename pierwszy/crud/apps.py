from django.apps import AppConfig
from .views import scrap_movies_script


class CrudConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crud'

    def ready(self):
        try:
            scrap_movies_script()
        except Exception as e:
            print(f"An error occured : {e}")
