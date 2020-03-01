from django.db import models


class Customer(models.Model):
    """
        "customerDetails": {
            "salutationCode": "02",
            "firstName": "Billie",
            "surname": "Jansen",
            "streetName": "Dorpstraat",
            "houseNumber": "1",
            "houseNumberExtended": "B",
            "addressSupplement": "Lorem Ipsum",
            "extraAddressInformation": "Apartment",
            "zipCode": "1111 ZZ",
            "city": "Utrecht",
            "countryCode": "NL",
            "email": "billie@verkopen.vnd.com",
            "company": "vnd.com",
            "vatNumber": "NL999999999B99",
            "chamberOfCommerceNumber": "99887766",
            "orderReference": "MijnReferentie",
            "deliveryPhoneNumber": "012123456"
          },
        "billingDetails": {
            "salutationCode": "02",
            "firstName": "Billie",
            "surname": "Jansen",
            "streetName": "Dorpstraat",
            "houseNumber": "1",
            "houseNumberExtended": "B",
            "addressSupplement": "Lorem Ipsum",
            "extraAddressInformation": "Apartment",
            "zipCode": "1111 ZZ",
            "city": "Utrecht",
            "countryCode": "NL",
            "email": "billie@verkopen.vnd.com",
            "company": "vnd.com",
            "vatNumber": "NL999999999B99",
            "chamberOfCommerceNumber": "99887766",
            "orderReference": "MijnReferentie",
            "deliveryPhoneNumber": "012123456"
          }
    """

    salutationCode = models.CharField(max_length=10, null=True, blank=True)
    firstName = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    streetName = models.CharField(max_length=55)
    houseNumber = models.CharField(max_length=20)
    houseNumberExtended = models.CharField(max_length=10, null=True, blank=True)
    addressSupplement = models.CharField(max_length=15, null=True, blank=True)
    extraAddressInformation = models.CharField(max_length=20, null=True, blank=True)
    zipCode = models.CharField(max_length=15)
    city = models.CharField(max_length=20)
    countryCode = models.CharField(max_length=10)
    email = models.EmailField()
    company = models.CharField(max_length=20, null=True, blank=True)
    vatNumber = models.CharField(max_length=20, null=True, blank=True)
    chamberOfCommerceNumber = models.CharField(max_length=15, null=True, blank=True)
    orderReference = models.CharField(max_length=20, null=True, blank=True)
    deliveryPhoneNumber = models.CharField(max_length=12, null=True, blank=True)

    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.firstName, self.surname)

    def __repr__(self):
        return f"<<{self.__class__.__name__}> email:{self.email}>"
