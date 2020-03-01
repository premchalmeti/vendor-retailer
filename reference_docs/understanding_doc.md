
**Requirements**

**Overview**

Step I: Write an app where the seller will add his shop

Step II: We will sync shipments for his shop

Step II: Store each data item from shipment detail


**Detailed overview**

Authentication

Add retailer shop API

**async**

Get all shipments
Store all shipments

Handle Access token expiry (after 5 minutes, auto refresh access-token)

API rate limiting

Validations and corner cases

RQ worker setup for background processing

Test cases for APIs

Host on cloud

Khushal:

Class-based views
OOPs
Middleware for token refresh
Client-id and Client-secret input from retailer
Get all shipments
Sync all shipments in pagination until empty response with rate limit
Trigger sync API for sync later


References:

https://developers.bol.com/

https://developers.bol.com/apiv3keyconcepts/

https://developers.bol.com/apiv3gettingstarted/

https://developers.bol.com/apiv3sellingonbolcomprocessflow/

Questions:

Who are the end-users of our app? a retailer user seems like retailer app uses my app
Store client_id and client_secret to refresh automatically right?
Looks like we are sending sensitive information and it is recommended to use https (TLS). Do I need to implement this as well?

Changes:

1. Add retry behaviour for failed jobs enqueue after 1 minutes
2. Change the ViewSet APIs to use the built-ins mixin functions
3. Use rq scheduler to schedule jobs at a given time
4. Implement the shipment details API

Sample API Responses:

url: /retailer/shipments
Response:
{
    "shipments": [
        {
            "shipmentId": 541757635,
            "shipmentDate": "2018-04-17T10:55:37+02:00",
            "shipmentReference": "BOLCOM001",
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
    ]
}
{
    'shipmentId': 719226009,
    'shipmentDate': '2020-02-11T09:22:32+01:00',
    'shipmentItems': [
        {'orderItemId': '2367494957', 'orderId': '2878188480'}
    ],
    'transport': {'transportId': 459463081}
}


url: /retailer/shipments/{shipment-id}
Response:
{
  "shipmentId": 541757635,
  "shipmentDate": "2018-04-17T10:55:37+02:00",
  "shipmentReference": "BOLCOM001",
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
      "offerReference": "BOLCOM00123",
      "fulfilmentMethod": "FBR"
    }
  ],
  "transport": {
    "transportId": 312778947,
    "transporterCode": "TNT",
    "trackAndTrace": "3SBOL0987654321",
    "shippingLabelId": 123456789,
    "shippingLabelCode": "PLR00000002"
  },
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
    "email": "billie@verkopen.bol.com",
    "company": "bol.com",
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
    "email": "billie@verkopen.bol.com",
    "company": "bol.com",
    "vatNumber": "NL999999999B99",
    "chamberOfCommerceNumber": "99887766",
    "orderReference": "MijnReferentie",
    "deliveryPhoneNumber": "012123456"
  }
}
