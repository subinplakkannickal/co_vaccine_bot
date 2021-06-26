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
        response = requests.get( self._get_states_url, headers=self._header)

        if response.status_code == 200:
            states = response.json()["states"]
            unordered_states = {state["state_id"]: state["state_name"] for state in states}
            ordered_states = dict(sorted(unordered_states.items()))
            return ordered_states

        elif response.status_code == 401:
            self.warning = "Unauthenticated access"
            return 0

        elif response.status_code == 500:
            self.warning = "Internal Server Error"
            return 0

    def get_districts(self, state_id):
        """ Get districts of given state in id order.
        """
        response = requests.get( self._get_district_id_url.format(state_id), headers=self._header)

        if response.status_code == 200:
            districts = response.json()["districts"]
            unordered_districts = {district["district_id"]: district["district_name"] for district in districts}
            ordered_districts = dict(sorted(unordered_districts.items()))
            return ordered_districts

        elif response.status_code == 401:
            self.warning = "Unauthenticated access"
            return 0

        elif response.status_code == 500:
            self.warning = "Internal Server Error"
            return 0

    def get_api_data_by_district_id_for_7days(self, district_id, vaccine_type):
        """ Get slots for 7 day in given district.
        args:
            district_id : int
            vaccine_type : str
        """
        date = utils.get_today()
        response = requests.get( self._calendar_by_district_url.format(
            district_id, date, vaccine_type), headers=self._header)
            
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