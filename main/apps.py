from django.apps import AppConfig
from django.contrib.auth import get_user_model
import logging
from django.db.utils import OperationalError, ProgrammingError

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        try:
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    password='admin123',
                    email='admin@example.com'
                )
                logging.warning("✔ נוצר משתמש סופר-יוזר בשם admin עם סיסמה admin123")
        except (OperationalError, ProgrammingError):
            # עדיין אין טבלאות – מתעלמים מהשגיאה
            pass

