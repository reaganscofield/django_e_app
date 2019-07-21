from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from chennels.auth import AuthMiddlewareStack
from chennels.security.websocket import AllowedHostsOriginValidator, AllowedHostsOriginValidator
from e_app.consumer import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^api/messages/(?P<sender>[0-9a-f-]+)/(?P<receiver>[0-9a-f-]+)/', ChatConsumer)
                ]
            )
        )
    )
})