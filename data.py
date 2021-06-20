import requests
import datetime
import time

class DATA(object):
    def __init__(self) -> None:
        super().__init__()
        self._calendar_by_district_url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}&vaccine={}"
        self._calendar_by_pincode_url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPincode?pincode={}&date={}&vaccine={}"
        self._get_states_url="https://cdn-api.co-vin.in/api/v2/admin/location/states"
        self._get_district_id_url="https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}"
        self._header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        self.pincode= []
        self.vaccine_type = ['COVISHIELD']

    def get_date(self, date_range=1):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=0)
        date_list = [start_date + datetime.timedelta(days=day) 
            for day in range(date_range)]
        return [date.strftime("%d-%m-%Y") for date in date_list]

    def get_states(self):
        states = requests.get( self._get_states_url, headers=self._header).json()["states"]
        return {state["state_name"]: state["state_id"] for state in states}

    def get_districts(self, state_id, district=None):
        districts = requests.get( self._get_district_id_url.format(state_id), headers=self._header).json()["districts"]
        district_dict = {district["district_name"]: district["district_id"] for district in districts}
        if district:
            return {district : district_dict[district]}
        return district_dict
    
    def get_api_data_by_pincode_for_7days(self, pincode):
        date = self.get_date()
        return ( requests.get( self._calendar_by_pincode_url.format(pincode, date, vaccine), headers=self._header).json() 
            for vaccine in self.vaccine_type for pincode in self.pincode 
            )

    def get_api_data_by_district_id_for_7days(self, district_id):
        date = self.get_date()
        return ( requests.get( self._calendar_by_district_url.format(district_id, date, vaccine), headers=self._header).json() 
            for vaccine in self.vaccine_type 
            )

# if "__main__" in __name__:
#     data = DATA()
#     result = data.get_api_data_by_district_id_for_7days('123')
#     for data in result:
#         for center in data['centers']:
#             print ("Center : {} {}\n=======================".format(center['name'], center['pincode']))
#             for session in center["sessions"]: 
#                 if session["available_capacity"] > 0:
#                     print ("{} D1: {} D2: {} <<<<<<<<<<<<<".format(session["date"], session["available_capacity_dose1"], session["available_capacity_dose2"]))
#                 else:
#                     print ("{} D1: {} D2: {}".format(session["date"], session["available_capacity_dose1"], session["available_capacity_dose2"]))
#             print ("=======================")
