from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import elearning.routing

application = ProtocolTypeRouter({
   'websocket': AuthMiddlewareStack(
       URLRouter(
           elearning.routing.websocket_urlpatterns
       )
   ),
})