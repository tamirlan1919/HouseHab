from django.apps import AppConfig

class UsersAppConfig(AppConfig):
    name = 'estatemaster'

    def ready(self):
        import estatemaster.signals  # Измените 'your_app.signals' на путь к вашему файлу с сигналами
