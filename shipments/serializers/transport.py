# built-in imports

# third-party imports
from rest_framework import serializers

# custom imports
from shipments.models import Transport


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['transportId', 'transporterCode', 'trackAndTrace', 'shippingLabelId', 'shippingLabelCode']
