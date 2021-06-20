import requests
import datetime
import time

class DATA(object):
    def __init__(self) -> None:
        super().__init__()
        self.url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}"
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    def get_date_list(self):
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=0)
        date_list = [start_date + datetime.timedelta(days=day) 
            for day in range(7)]
        return [date.strftime("%d-%m-%Y") for date in date_list]

    def get_pincode(self):
        return ['670511', '670305', '670571', '671326']

    def get_vaccine_type(self):
        return ["COVISHIELD"]

    def get_api_data(self):
        date_list = self.get_date_list()
        vaccine_type = self.get_vaccine_type()
        pincode_list = self.get_pincode()
        return ( requests.get( self.url.format(pincode, date), headers=self.header).json() 
            for vaccine in vaccine_type for date in date_list for pincode in pincode_list  
            )

if "__main__" in __name__:
    data = DATA()
    result = data.get_api_data()
    for data in result:
        for session in data['sessions']:
            if session["available_capacity"] > 0: 
                print ("{} : {} : {} <<<<<".format(session["date"], session["name"], session["available_capacity"]))
            else:
                print ("{} : {} : {}".format(session["date"], session["name"], session["available_capacity"]))
                
            time.sleep(3)


