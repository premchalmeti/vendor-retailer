# built-in imports

# third-party imports
from rest_framework import serializers

# custom imports
from shipments.models import Order


class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data, *args, **kwargs):
        """
            Overridden create() method for associating `shipment` with `orders`

            :param validated_data: validated data after passed through all validators
            :param args: positional parameters
            :param kwargs: keyword arguments
            :return: `Order` instance newly created
        """
        shipment_instance = self._context.get('shipment_instance', None)
        validated_data['shipment'] = shipment_instance
        os = Order.objects.create(**validated_data)
        return os

    class Meta:
        model = Order
        fields = [
            'orderItemId', 'orderId', 'orderDate', 'latestDeliveryDate', 'ean', 'title', 'quantity',
            'offerPrice', 'offerCondition', 'offerReference', 'fulfilmentMethod'
        ]
