import requests
from utils import utils, url

class SearchByDistrict(object):
    """ Class for search vaccination slots by district.
    """
    def __init__(self):
        self._calendar_by_district_url = url.CALENDAR_BY_DISTICT_URL
        self._get_states_url = url.GET_STATES_URL
        self._get_district_id_url = url.GET_DISTRICT_ID_URL
        self._header = url.HEADER
        self.warning = None

    def get_states(self):
        """ Get states in id order.
        """
        response = utils.get_api_response( self._get_states_url, headers=self._header)

        if response.response:
            return response.response

        else:
            self.warning = response.warning
            return 0

    def get_districts(self, state_id):
        """ Get districts of given state in id order.
        """
        response = utils.get_api_response( self._get_district_id_url.format(state_id), headers=self._header)

        if response.response:
            return response.response

        else:
            self.warning = response.warning
            return 0

    def get_api_data_by_district_id_for_7days(self, district_id, vaccine_type):
        """ Get slots for 7 day in given district.
        args:
            district_id : int
            vaccine_type : str
        """
        date = utils.get_today()
        response = utils.get_api_response( self._calendar_by_district_url.format(
            district_id, date, vaccine_type), headers=self._header)
            
        if response.response:
            return response.response

        else:
            self.warning = response.warning
            return 0