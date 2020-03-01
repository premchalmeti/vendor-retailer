# Define project specific custom exceptions in this module


class ThirdPartyAPIException(Exception):
    """
    This is a custom exception class for handling 'bol.com' API Response gracefully
    """

    def __init__(self, response_obj, *args, **kwargs):
        self.res_obj = response_obj
        super().__init__(*args, **kwargs)

    def get_json_res(self):
        return self.res_obj.json()

    @property
    def status_code(self):
        return self.res_obj.status_code
