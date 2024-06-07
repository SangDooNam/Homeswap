"""
ASGI config for homeswap project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from messaging.routing import websocket_urlpatterns
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount, Route
from starlette.applications import Starlette

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeswap.settings')

django_asgi_app = get_asgi_application()


starlette_app = Starlette(routes=[
    Mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'staticfiles')), name="static"),
    Mount("/", app=django_asgi_app),
])

application = ProtocolTypeRouter({
    "http": starlette_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})





