from django.apps import AppConfig

# class MainConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'main'

class MainConfig(AppConfig):
    name = 'recommender'

    def ready(self):
        from jobs import updater
        updater.start()
