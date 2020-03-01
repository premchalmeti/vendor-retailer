# built-in imports

# third-party imports
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

# custom imports


urlpatterns = [
    path('', RedirectView.as_view(
        pattern_name='retailers:retailers-list', permanent=False)
    ),
    path('admin/', admin.site.urls),

    # `retailers` urls
    path('api/', include('retailers.urls', namespace='retailers')),

    # `shipments` urls
    path('api/retailers/<int:pk>/', include('shipments.urls', namespace='shipments'))
]
