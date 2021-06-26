import requests
from utils import utils, url
class SearchByPincode(object):
    """ Class for search vaccination slots by pincode.
    """
    def __init__(self) -> None:
        self._calendar_by_pincode_url = url.CALENDAR_BY_PINCODE_URL
        self._header = url.HEADER
        self.warning = None
        
    def get_api_data_by_pincode_for_7days(self, pincode, vaccine_type):
        """ Get slots for 7 day in given district.
        args:
            pincode : int
            vaccine_type : str
        """
        date = utils.get_today()
        response = requests.get( self._calendar_by_pincode_url.format(
            pincode, date, vaccine_type), headers=self._header)
            
        if response.status_code == 200:
            return response.json()

        elif response.status_code == 400:
            self.warning = "Bad Request"
            return 0

        elif response.status_code == 401:
            self.warning = "Unauthenticated access"
            return 0

        elif response.status_code == 500:
            self.warning = "Internal Server Error"
            return 0