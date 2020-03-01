# built-in imports

# third-party imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

# custom imports
from vendor_retailer.exceptions import ThirdPartyAPIException
from retailers.models import Retailer
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer


class ShipmentRateThrottle(UserRateThrottle):
    """
    Scoped throttle class with Rate limit of `7 requests/minute per user`
    """
    scope = 'SHIPMENTS'


class ShipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This is ViewSet class responsible for,
    `list` (shipments), `retrieve`(shipment details), `destroy` (shipment) and
    `sync` (shipments)
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    lookup_field = 'shipmentId'

    throttle_classes = [ShipmentRateThrottle]

    def get_queryset(self):
        retailer = self.kwargs['pk']
        return self.queryset.filter(retailer=retailer)

    @action(detail=False, methods=['GET'])
    def sync(self, request, pk=None, *args, **kwargs):
        """
        This is shipment sync API for given retailer.

        The flow of this API is,
            Authorize (get access_token) -> Sync shipments (for both fulfilment-types) -> Serialize and save shipments

        :param request: django `HttpRequest` instance
        :param pk: pk is `pk` attribute of `Retailer` instance
        :return: Rest `response` instance

        """

        if not pk:
            return Response({'detail': "Please give retailer to sync"}, status=status.HTTP_400_BAD_REQUEST)
        elif not Retailer.objects.filter(id=pk).exists():
            return Response({'detail': "Retailer not found"}, status=status.HTTP_404_NOT_FOUND)

        from .managers import ShipmentManager

        try:
            shipment_mgr = ShipmentManager(retailer_id=pk)

            q = shipment_mgr.q_obj

            func = shipment_mgr.fetch_list

            q.enqueue(
                func, retailer_id=pk,
                page=1, fulfilment_method=Shipment.FULFILLED_BY_VENDOR
            )
            q.enqueue(
                func, retailer_id=pk,
                page=1, fulfilment_method=Shipment.FULFILLED_BY_RETAILER
            )

        except ThirdPartyAPIException as api_exc:
            return Response(data=api_exc.get_json_res(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                data={'detail': 'Sync Started'},
                status=status.HTTP_200_OK
            )
