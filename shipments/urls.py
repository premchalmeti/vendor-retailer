# built-in imports

# third-party imports
from rest_framework import routers

# custom imports
from . import views

app_name = 'shipments'

shipments_router = routers.SimpleRouter()
shipments_router.register('shipments', views.ShipmentViewSet, basename='shipments')

urlpatterns = shipments_router.urls
