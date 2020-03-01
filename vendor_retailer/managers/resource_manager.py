from abc import ABCMeta, abstractmethod

from vendor_retailer.utils import get_or_create_queue
from retailers.managers import RetailerManager


class ResourceManager(metaclass=ABCMeta):
    Q_NAME = 'default'
    THROTTLE_SCOPE = 'user'

    def __init__(self, retailer_id):
        self.retailer_mgr = RetailerManager(retailer_id=retailer_id)
        self.common_headers = {
            'Accept': 'application/vnd.retailer.v3+json',
            'Authorization': 'Bearer {auth-token}'
        }
        self.q_obj = get_or_create_queue(self.Q_NAME)
        self.serializer_class = None

    def get_signed_header(self):
        self.common_headers['Authorization'] = f'Bearer {self.retailer_mgr.token}'
        return self.common_headers

    def create_resource(self, data, ctx):
        assert self.serializer_class is not None,
            "You must set `serializer_class` before creating any resource"
        serializer_obj = self.serializer_class(data=data, context=ctx)
        if serializer_obj.is_valid():
            serializer_obj.save()
        else:
            raise ValueError(serializer_obj.errors)

    @abstractmethod
    def check_resource_exists(self, *args, **kwargs):
        pass

    @abstractmethod
    def fetch_list(self, *args, **kwargs):
        pass

    @abstractmethod
    def fetch_detail(self, *args, **kwargs):
        pass
