"""
ASGI config for chathome project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os, django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat_control.route import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from chat_control.channels_middleware import JWTWebsocketMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chathome.settings")
django.setup()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTWebsocketMiddleware(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
