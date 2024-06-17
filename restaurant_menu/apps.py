from django.apps import AppConfig


class ResturantMenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant_menu'
    
    def ready(self):
        import restaurant_menu.signals
        