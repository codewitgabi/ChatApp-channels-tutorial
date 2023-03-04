import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_app = get_asgi_application()

from chat import routers as chat_routers
from main import routers as main_routers

application = ProtocolTypeRouter({
	"http": django_asgi_app,
	"websocket": AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(
				chat_routers.websocket_urlpatterns + 
				main_routers.websocket_urlpatterns
			)
		)
	)
})
