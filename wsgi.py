import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings


settings.DEBUG = False
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarly.settings')

application = get_wsgi_application()