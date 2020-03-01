from django.db import models

from .shipment import Shipment


class Order(models.Model):
    """
        shipments contains ShipmentItems (orders)
        "shipmentItems": [
            {
                "orderItemId": "1234567891",
                "orderId": "4123456789"
            }
        ]

        "shipmentItems": [
            {
              "orderItemId": "1234567891",
              "orderId": "4123456789",
              "orderDate": "2018-04-17T10:55:37+02:00",
              "latestDeliveryDate": "2018-04-20T10:55:37+02:00",
              "ean": "0000007740404",
              "title": "Product Title",
              "quantity": 10,
              "offerPrice": 12.99,
              "offerCondition": "NEW",
              "offerReference": "VNDCOM00123",
              "fulfilmentMethod": "FBR"
            }
          ]
    """
    NEW = "NEW"
    OLD = "OLD"
    AS_NEW = "AS_NEW"
    GOOD = "GOOD"
    REASONABLE = "REASONABLE"
    MODERATE = "MODERATE"

    OFFER_CONDITION_TYPES = (
        (NEW, "NEW"),
        (OLD, "OLD"),
        (AS_NEW, "AS_NEW"),
        (GOOD, "GOOD"),
        (REASONABLE, "REASONABLE"),
        (MODERATE, "MODERATE")
    )

    orderItemId = models.CharField(max_length=10)
    orderId = models.CharField(max_length=10)

    shipment = models.ForeignKey('shipment', on_delete=models.CASCADE,
                                 related_name='shipmentItems', related_query_name='shipmentItems')

    # `Shipment` Details data
    orderDate = models.DateTimeField()
    latestDeliveryDate = models.DateTimeField()
    ean = models.CharField(max_length=13)
    title = models.CharField(max_length=120)
    quantity = models.IntegerField()
    offerPrice = models.FloatField()
    offerCondition = models.CharField(choices=OFFER_CONDITION_TYPES, max_length=3)
    offerReference = models.CharField(max_length=15, null=True, blank=True)
    fulfilmentMethod = models.CharField(choices=Shipment.SHIPMENT_FULFILMENT_TYPES, max_length=3)

    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Shipment ID %s, Order ID %s" % (self.shipment.shipmentId, self.orderId)

    def __repr__(self):
        return f"<<{self.__class__.__name__}> Id:{self.orderItemId} Shipment-Id:{self.shipment.shipmentId}>"
