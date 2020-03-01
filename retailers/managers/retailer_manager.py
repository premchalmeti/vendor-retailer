# built-in imports
# note: to avoid conflict between outer `datetime` package and `datetime.datetime` inner module
#       import `datetime` as `dt` alias
import datetime as dt

import requests
# third-party imports
from dateutil import parser
from django.conf import settings

# custom imports
from vendor_retailer.exceptions import ThirdPartyAPIException
from vendor_retailer.utils import get_redis_connection
from retailers.models import Retailer


class RetailerManager(object):
    """
        This manager class is responsible for `Retailer` and contains all logic for authorize,
        re-authorize and sync shipments
    """

    def __init__(self, client_id=None, client_secret=None, retailer_obj=None, retailer_id=None):

        self._init_from_params(client_id, client_secret, retailer_obj, retailer_id)
        self.redis_auth_key = f'{self.retailer_obj.clientId}_auth'

        # `vendor.com` authorization request meta info
        self._auth_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        self.auth_url = getattr(settings, 'OAUTH_LOGIN_URL', 'https://login.vendor.com/token')
        self.auth_res_json = None

        self.redis_store = get_redis_connection()

    def _init_from_params(self, client_id, client_secret, retailer_obj, retailer_id):
        # retrieve `Retailer` instance from either of <client_id|client_secret>, <retailer_id> or <retailer_obj>
        # parameters
        if retailer_obj:
            self.retailer_obj = retailer_obj
        elif client_secret and client_secret:
            self.retailer_obj = Retailer.objects.filter(
                clientId=client_id, clientSecret=client_secret
            ).first()
        elif retailer_id:
            self.retailer_obj = Retailer.objects.filter(id=retailer_id).first()
        else:
            raise ValueError('Incorrect arguments passed. Provide at least <client_id|client_secret> or' +
                             '<retailer_obj> or <retailer_id> as parameter')

    def authorize(self):
        __payload = {
            'client_id': self.retailer_obj.clientId,
            'client_secret': self.retailer_obj.clientSecret,
            'grant_type': 'client_credentials'
        }

        resp_obj = requests.post(
            self.auth_url, data=__payload, headers=self._auth_headers
        )

        if not resp_obj.ok:
            raise ThirdPartyAPIException(resp_obj)

        self.auth_res_json = resp_obj.json()
        self.store_token_meta()
        return self.auth_res_json

    def is_auth_needed(self):
        """
            :return:
                True if `access_token` if token not found or token is expired
                False if `access_token` if found and alive is cache
        """
        expiry_date = self.get_from_cache('expiry_date')
        token = self.get_from_cache('token')
        return not token or (expiry_date and parser.parse(expiry_date) <= dt.datetime.utcnow())

    def store_token_meta(self):
        expiry_date_obj = dt.datetime.utcnow() + dt.timedelta(seconds=self.auth_res_json['expires_in'])

        retailer_auth_res = {
            'token': self.auth_res_json['access_token'],
            'expiry_date': expiry_date_obj.isoformat(),
            'expires_in': self.auth_res_json['expires_in'],
            'token_type': self.auth_res_json['token_type'],
            'scope': self.auth_res_json['scope']
        }

        self.redis_store.hmset(self.redis_auth_key, retailer_auth_res)

    def get_from_cache(self, key):
        key = key.encode()
        value = self.redis_store.hgetall(self.redis_auth_key).get(key)
        return value.decode('utf-8') if value else None

    @property
    def token(self):
        """
            return retailer's `access_token` from redis
        :return:
        """
        if self.is_auth_needed():
            self.authorize()

        return self.get_from_cache('token')
