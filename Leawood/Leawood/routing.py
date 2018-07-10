# Leawood/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.routing import ChannelNameRouter
import main.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
    'channel': ChannelNameRouter({
		"test_channel": main.consumers.DeviceChannelConsumer,
    }),
})
