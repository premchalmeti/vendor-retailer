# built-in imports

# third-party imports
from django.contrib import admin

# custom imports
from .models import (
    Order, Transport, Shipment
)

# Register your models here.

admin.site.register(Order)
admin.site.register(Shipment)
admin.site.register(Transport)
