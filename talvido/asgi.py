import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from chat import routings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talvido.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routings.websocket_urlpatterns
        )
    ),
})
