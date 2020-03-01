from django.db import models


class Shipment(models.Model):
    FULFILLED_BY_VENDOR = 'FBV'
    FULFILLED_BY_RETAILER = 'FBR'

    SHIPMENT_FULFILMENT_TYPES = (
        (FULFILLED_BY_VENDOR, 'Fulfilled By Vendor'),
        (FULFILLED_BY_RETAILER, 'Fulfilled By Retailer'),
    )

    shipmentId = models.IntegerField()
    shipmentDate = models.DateTimeField()

    # `shipment_reference` may be null for shipments fulfilled by `FBR`
    shipmentReference = models.CharField(max_length=30, blank=True, null=True)

    fulfilmentMethod = models.CharField(max_length=3, choices=SHIPMENT_FULFILMENT_TYPES,
                                        default=FULFILLED_BY_RETAILER)

    retailer = models.ForeignKey('retailers.Retailer', on_delete=models.CASCADE)
    transport = models.ForeignKey('transport', on_delete=models.CASCADE)

    customerDetails = models.ForeignKey(
        'customer', on_delete=models.CASCADE, related_query_name='customerDetails', related_name='customerDetails'
    )
    billingDetails = models.ForeignKey(
        'customer', on_delete=models.CASCADE, related_query_name='billingDetails', related_name='billingDetails'
    )

    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    @classmethod
    def create_from_json(cls, json_data):
        pass

    def __str__(self):
        return "Shipment ID %s, Reference %s" % (self.shipmentId, self.shipmentReference)

    def __repr__(self):
        return f"<<{self.__class__.__name__}> Id:{self.shipmentId} Ref:{self.shipmentReference}>"
