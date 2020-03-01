from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from retailers.tests import create_retailer
from .serializers import ShipmentSerializer


def create_shipment(shipment_json, retailer):
    sp = ShipmentSerializer(data=shipment_json, context={
        'retailer_instance': retailer
    })
    if sp.is_valid():
        sp.save()
    return sp.instance


class ShipmentTestCase(TestCase):

    def setUp(self):
        self.assertIs(hasattr(settings, 'VENDOR_TEST_CLIENT_ID'), True)
        self.assertIs(hasattr(settings, 'VENDOR_TEST_CLIENT_SECRET'), True)

        self.clientId = getattr(settings, 'VENDOR_TEST_CLIENT_ID')

        self.clientSecret = getattr(settings, 'VENDOR_TEST_CLIENT_SECRET')

        self.shipment_json = {
            "shipmentId": 541757635,
            "shipmentDate": "2018-04-17T10:55:37+02:00",
            "shipmentReference": "VNDCOM001",
            "shipmentItems": [
                {
                    "orderItemId": "1234567891",
                    "orderId": "4123456789"
                }
            ],
            "transport": {
                "transportId": 312778947
            }
        }
        self.retailer_obj = create_retailer(self.clientId, self.clientSecret)

    def test_create_shipment(self):
        shipment = create_shipment(self.shipment_json, self.retailer_obj)
        self.assertIsNotNone(shipment)
        self.assertIs(self.retailer_obj.shipment_set.filter(id=shipment.id).exists(), True)

    def test_shipment_throttle(self):
        throttle_limit = 7

        url = reverse('retailers:shipments:shipments-list', args=(self.retailer_obj.id,))

        for req_time in range(throttle_limit):
            self.client.get(url)

        # this response should be 429 - too many requests
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
