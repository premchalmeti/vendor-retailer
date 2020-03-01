# built-in imports
import requests
# third-party imports
from django.conf import settings

# custom imports
from vendor_retailer.exceptions import ThirdPartyAPIException
from vendor_retailer.managers import ResourceManager
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
from shipments.views import ShipmentRateThrottle


class ShipmentManager(ResourceManager):
    """
    This manager class is responsible for `Shipments` and contains all logic for sync, create shipments
    """
    Q_NAME = 'shipment_q'

    def __init__(self, retailer_id):
        super().__init__(retailer_id)

        self.retailer_id = retailer_id
        self.resource_list_API = getattr(
            settings, 'VENDOR_SHIPMENT_LIST_API', 'https://api.bol.com/retailer/shipments/'
        )

        self.resource_detail_API = getattr(
            settings, 'VENDOR_SHIPMENT_DETAIL_API', 'https://api.bol.com/retailer/shipments/{shipment_id}'
        )
        self.serializer_class = ShipmentSerializer
        self.rate_limit_duration = ShipmentRateThrottle().duration

    @classmethod
    def fetch_list(cls, retailer_id, page, fulfilment_method):
        """

            This function is responsible for fetching list of shipments for a given fulfilment-method
            and call their details API to create shipments which not already exists

            :param retailer_id: Retailer's `pk` to associate shipments with
            :param page: This is `current_page` on of the pagination parameter
            :param fulfilment_method:
                Refer `Shipment` model to check available fulfilment-methods
            :return:

        """
        shipment_mgr = cls(retailer_id)
        q_obj = shipment_mgr.q_obj
        _params = {
            'page': page,
            'fulfilment-method': fulfilment_method
        }

        res = requests.get(
            url=shipment_mgr.resource_list_API, params=_params, headers=shipment_mgr.get_signed_header()
        )
        data = res.json()

        if not res.ok:
            raise ThirdPartyAPIException(res)
        elif res.ok and data:
            shipment_ids = [shipment['shipmentId'] for shipment in data['shipments']]

            shipment_mgr.get_resource_details(resource_ids=shipment_ids, fulfilment_method=fulfilment_method)

            job = q_obj.enqueue(cls.fetch_list, retailer_id=retailer_id,
                                page=page + 1, fulfilment_method=fulfilment_method)

            job.meta['rate_limit'] = shipment_mgr.rate_limit_duration
            job.save_meta()

    @classmethod
    def fetch_detail(cls, retailer_id, shipment_id, fulfilment_method):
        """
            This is shipment details API. Responsibilities includes fetch details and store in db

            :param retailer_id: Retailer's `pk` to associate shipments with
            :param shipment_id: This is `current_page` on of the pagination parameter
            :param fulfilment_method: Refer `Shipment` model to check available fulfilment-methods
            :return: None
        """

        shipment_mgr = cls(retailer_id)

        res = requests.get(
            url=shipment_mgr.resource_detail_API.format(shipment_id=shipment_id),
            headers=shipment_mgr.get_signed_header()
        )
        data = res.json()

        if not res.ok:
            raise ThirdPartyAPIException(res)
        elif res.ok and data:
            data['fulfilmentMethod'] = fulfilment_method
            ctx = {
                'retailer_instance': shipment_mgr.retailer_mgr.retailer_obj
            }
            shipment_mgr.create_resource(data, ctx)

    def check_resource_exists(self, shipment_id):
        return Shipment.objects.filter(retailer__id=self.retailer_id, shipmentId=shipment_id).exists()

    def get_resource_details(self, resource_ids, fulfilment_method):
        # Enqueue call shipment details api for shipments which not already exists in db
        for resource_id in resource_ids:
            if not self.check_resource_exists(resource_id):
                job = self.q_obj.enqueue(
                    self.fetch_detail, retailer_id=self.retailer_id, shipment_id=resource_id,
                    fulfilment_method=fulfilment_method
                )
                job.meta['rate_limit'] = self.rate_limit_duration
                job.save_meta()
