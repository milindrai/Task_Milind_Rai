import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospital_management.settings")

from django.core.asgi import get_asgi_application
app = get_asgi_application()