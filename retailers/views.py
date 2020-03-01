# built-in imports

# third-party imports
from django.shortcuts import get_object_or_404
from rest_framework import (status, viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response

# custom imports
from vendor_retailer.exceptions import ThirdPartyAPIException
from .managers import RetailerManager
from .models import Retailer
from .serializers import RetailerSerializer


class RetailerViewSet(viewsets.ModelViewSet):
    """
    This is ViewSet class responsible for,
    `list` (retailers), `retrieve`(retailer details), `destroy` (retailer) and
    `authorize` (retailer)
    """
    serializer_class = RetailerSerializer
    queryset = Retailer.objects.all()

    @action(methods=['GET'], detail=True)
    def authorize(self, request, pk=None, *args, **kwargs):
        """
            :param request: django `HttpRequest` instance
            :param pk: `pk` attribute of `Retailer` instance
            :param args: positional parameters
            :param kwargs: keyword arguments
            :return:
                status 200 if authorization successful
                status 400 on authorization failure
        """
        retailer_obj = get_object_or_404(Retailer, pk=pk)
        retail_mgr = RetailerManager(retailer_obj=retailer_obj)

        try:
            retail_mgr.authorize()
        except ThirdPartyAPIException as api_exc:
            return Response(data=api_exc.get_json_res(), status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"detail": "Authorization successful"}, status=status.HTTP_200_OK)
