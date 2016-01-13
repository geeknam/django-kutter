import os
from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{project_name}}.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

application = get_wsgi_application()
