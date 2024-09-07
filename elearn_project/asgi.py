import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter

import elearning.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearn_project.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            elearning.routing.websocket_urlpatterns
        )
    ),
})

ASGI_APPLICATION = 'elearn_project.asgi.application'

