# built-in imports

# third-party imports
from rest_framework import serializers

# custom imports
from shipments.models import (Shipment, Transport, Customer)
from .customer import CustomerSerializer
from .order import OrderSerializer
from .transport import TransportSerializer


class ShipmentSerializer(serializers.ModelSerializer):
    transport = TransportSerializer()

    shipmentItems = OrderSerializer(many=True)

    customerDetails = CustomerSerializer()
    billingDetails = CustomerSerializer()

    def create(self, validated_data, *args, **kwargs):
        """
        Overridden create() method for,
            create or get `Transport` instance
            create `Shipment` instance then
            create associated `ShipmentItems`(orders) of Shipment

        :param validated_data: validated data after passed through all validators
        :param args:
        :param kwargs:
        :return:

        """
        # todo: check if can move following create() functions to seperate models
        transport = validated_data.pop('transport', {})

        transport_obj = Transport.objects.filter(transportId=transport['transportId']).first()

        if not transport_obj:
            ts = TransportSerializer(data=transport)

            if ts.is_valid():
                ts.save()
                transport_obj = ts.instance
            else:
                raise ValueError(ts.errors)

        validated_data['transport'] = transport_obj

        customer = validated_data.pop('customerDetails', {})

        cust_obj = Customer.objects.filter(email=customer['email']).first()

        if not cust_obj:
            cust = CustomerSerializer(data=customer)

            if cust.is_valid():
                cust.save()
                cust_obj = cust.instance
            else:
                raise ValueError(cust.errors)

        validated_data['customerDetails'] = cust_obj

        billing = validated_data.pop('billingDetails', {})

        billing_obj = Customer.objects.filter(email=billing['email']).first()

        if not billing_obj:
            billing = CustomerSerializer(data=billing)

            if billing.is_valid():
                billing.save()
                billing_obj = billing.instance
            else:
                raise ValueError(billing.errors)

        validated_data['billingDetails'] = billing_obj

        # associate `Retailer` with `Shipment`
        validated_data['retailer'] = self._context.get('retailer_instance', None)
        orders = validated_data.pop('shipmentItems', [])
        shipment_obj = Shipment.objects.create(**validated_data)

        # create associated `shipmentItems` (orders)
        os = OrderSerializer(data=orders, many=True, context={
            'shipment_instance': shipment_obj
        })

        if os.is_valid():
            os.save()
        else:
            raise ValueError(os.errors)

        return shipment_obj

    class Meta:
        model = Shipment
        fields = ['shipmentId', 'shipmentDate', 'shipmentReference', 'shipmentItems', 'fulfilmentMethod',
                  'transport', 'customerDetails', 'billingDetails']
        depth = 1
