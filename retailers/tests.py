from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Retailer


# Create your tests here.


def create_retailer(clientId, clientSecret):
    return Retailer.objects.create(name="Dummy Retailer", clientId=clientId, clientSecret=clientSecret)


class RetailerTestCase(TestCase):

    def setUp(self):
        self.assertIs(hasattr(settings, 'VENDOR_TEST_CLIENT_ID'), True)
        self.assertIs(hasattr(settings, 'VENDOR_TEST_CLIENT_SECRET'), True)

        self.clientId = getattr(settings, 'VENDOR_TEST_CLIENT_ID')

        self.clientSecret = getattr(settings, 'VENDOR_TEST_CLIENT_SECRET')

    def test_retailer_created_api(self):
        _payload = {
            "name": "Dummy retailer",
            "clientId": self.clientId,
            "clientSecret": self.clientSecret
        }
        response = self.client.post(reverse('retailers:retailers-list'), _payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Retailer.objects.filter(clientId=self.clientId, clientSecret=self.clientSecret).exists(), True)

    def test_retailer_list_api(self):
        retailer = create_retailer(self.clientId, self.clientSecret)
        response = self.client.get(reverse('retailers:retailers-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, retailer.id)

    def test_retailer_detail_api(self):
        retailer = create_retailer(self.clientId, self.clientSecret)

        url = reverse('retailers:retailers-detail', args=(retailer.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, retailer.id)
