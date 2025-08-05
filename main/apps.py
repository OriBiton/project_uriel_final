from django.apps import AppConfig
from django.contrib.auth import get_user_model
import logging

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='0544403199',
                password='Ori192837465',
                email='admin@example.com'
            )
            logging.warning("✔ נוצר משתמש סופר-יוזר בשם admin עם סיסמה admin123")

