import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarly.settings')
os.environ.setdefault('DEBUG', 'False')

application = get_wsgi_application()