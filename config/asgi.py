"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


django_asgi_app = get_asgi_application()

from monitoring.consumers import mqttConsumer, StreamConsumer

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # mqtt handler
        "mqtt": mqttConsumer.as_asgi(),
        'websocket': URLRouter([path('practice', StreamConsumer.as_asgi())])
    }

