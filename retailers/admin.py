# built-in imports

# third-party imports
from django.contrib import admin

# custom imports
from .models import (
    Retailer
)

# Register your models here.
admin.site.register(Retailer)
