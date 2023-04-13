"""
ASGI config for talvido project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from .settings.base import DEBUG
from django.core.asgi import get_asgi_application

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talvido.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talvido.settings.production')

application = get_asgi_application()
