# built-in imports

# third-party imports
from rest_framework import serializers

# custom imports
from shipments.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "salutationCode",
            "firstName",
            "surname",
            "streetName",
            "houseNumber",
            "houseNumberExtended",
            "addressSupplement",
            "extraAddressInformation",
            "zipCode",
            "city",
            "countryCode",
            "email",
            "company",
            "vatNumber",
            "chamberOfCommerceNumber",
            "orderReference",
            "deliveryPhoneNumber"
        ]
