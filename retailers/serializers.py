# built-in imports

# third-party imports
from rest_framework.serializers import ModelSerializer

# custom imports
from .models import Retailer


class RetailerSerializer(ModelSerializer):
    class Meta:
        model = Retailer
        fields = ['id', 'name', 'clientId', 'clientSecret']
