import os
import django
from django.core.wsgi import get_wsgi_application

print("💡 WSGI start loading...")  # שורת בדיקה

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

application = get_wsgi_application()
