from rest_framework import routers

from . import views

app_name = 'retailers'

retailers_router = routers.SimpleRouter()
retailers_router.register('retailers', views.RetailerViewSet, basename='retailers')

urlpatterns = retailers_router.urls
