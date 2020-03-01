from django.db import models


class Transport(models.Model):
    """
        shipments contains transport_id (312778947)

        "transport": {
            "transportId": 312778947,
            "transporterCode": "TNT",
            "trackAndTrace": "3SVND0987654321",
            "shippingLabelId": 123456789,
            "shippingLabelCode": "PLR00000002"
        }
    """

    BRIEFPOST = 'BRIEFPOST'
    UPS = 'UPS'
    TNT = 'TNT'
    TNT_EXTRA = 'TNT_EXTRA'
    TNT_BRIEF = 'TNT_BRIEF'
    TNT_EXPRESS = 'TNT_EXPRESS'
    DYL = 'DYL'
    DPD_NL = 'DPD_NL'
    DPD_BE = 'DPD_BE'
    BPOST_BE = 'BPOST_BE'
    BPOST_BRIEF = 'BPOST_BRIEF'
    DHLFORYOU = 'DHLFORYOU'
    GLS = 'GLS'
    FEDEX_NL = 'FEDEX_NL'
    FEDEX_BE = 'FEDEX_BE'
    OTHER = 'OTHER'
    DHL = 'DHL'
    DHL_DE = 'DHL_DE'
    DHL_GLOBAL_MAIL = 'DHL_GLOBAL_MAIL'
    TSN = 'TSN'
    FIEGE = 'FIEGE'
    TRANSMISSION = 'TRANSMISSION'
    PARCEL_NL = 'PARCEL_NL'
    LOGOIX = 'LOGOIX'
    PACKS = 'PACKS'
    COURIER = 'COURIER'
    RJP = 'RJP'

    TRANSPORTED_CODE_CHOICES = (
        (BRIEFPOST, 'BRIEFPOST'),
        (UPS, 'UPS'),
        (TNT, 'TNT'),
        (TNT_EXTRA, 'TNT_EXTRA'),
        (TNT_BRIEF, 'TNT_BRIEF'),
        (TNT_EXPRESS, 'TNT_EXPRESS'),
        (DYL, 'DYL'),
        (DPD_NL, 'DPD_NL'),
        (DPD_BE, 'DPD_BE'),
        (BPOST_BE, 'BPOST_BE'),
        (BPOST_BRIEF, 'BPOST_BRIEF'),
        (DHLFORYOU, 'DHLFORYOU'),
        (GLS, 'GLS'),
        (FEDEX_NL, 'FEDEX_NL'),
        (FEDEX_BE, 'FEDEX_BE'),
        (OTHER, 'OTHER'),
        (DHL, 'DHL'),
        (DHL_DE, 'DHL_DE'),
        (DHL_GLOBAL_MAIL, 'DHL_GLOBAL_MAIL'),
        (TSN, 'TSN'),
        (FIEGE, 'FIEGE'),
        (TRANSMISSION, 'TRANSMISSION'),
        (PARCEL_NL, 'PARCEL_NL'),
        (LOGOIX, 'LOGOIX'),
        (PACKS, 'PACKS'),
        (COURIER, 'COURIER'),
        (RJP, 'RJP')
    )

    transportId = models.CharField(max_length=9)

    transporterCode = models.CharField(choices=TRANSPORTED_CODE_CHOICES, max_length=20)
    trackAndTrace = models.CharField(max_length=20, null=True, blank=True)
    shippingLabelId = models.CharField(max_length=40, null=True, blank=True)
    shippingLabelCode = models.CharField(max_length=15, null=True, blank=True)

    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Transport ID %s" % self.transportId

    def __repr__(self):
        return f"<<{self.__class__.__name__}> Id: {self.transportId}>"
