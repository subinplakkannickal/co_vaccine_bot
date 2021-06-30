import sys
import os
import json
from copy import deepcopy
from hashlib import sha256
import time
from utils import utils
from data.authentication import Authentication
from search_vaccine_slotes_by_districts import SearchVaccineSlotesByDistricts
from search_vaccine_slotes_by_pincode import SearchVaccineSlotesByPincode

class CoVaccineBot(object):
    def __init__(self):
        self.authentication = Authentication()
        self._preference_modified = False

    def read_json(self, mobile_number):
        """ Read user json file from /home/${user}/tmp/co_vaccine_bot/
        args:
            mobile_number: int
        """
        file_name = "/home/{}/tmp/co_vaccine_bot/{}.json".format(os.getlogin(), mobile_number)
        if not os.path.exists(file_name):
            return {}

        with open(file_name, "r") as f:
            data = json.load(f)

        return data

    def update_json(self, mobile_number, data):
        """ Update user json file data.
        """
        file_name = "/home/{}/tmp/co_vaccine_bot/{}.json".format(os.getlogin(), mobile_number)
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        with open(file_name, "w") as f:
            json.dump(data, f, sort_keys=True, indent=4)

        utils.message("{} updated with {}".format(file_name, data.items()))
        
    def main(self):
        utils.message("CO VACCINE BOT started")
        # Get user inputs
        while True:
            mobile_number = input("Enter registered mobile number: ")
            if len(mobile_number) == 10 and mobile_number.isnumeric():
                break
            else:
                utils.warning("Invalid mobile number")
                if not input("Do you want contineue? y/n ") == "y":
                    break
        
        user_data = self.read_json(mobile_number)
        
        if user_data:
            prefernce = True
            utils.message("User preference found.")
            user_confirmation = input(
                "Do you continue with previous preference? y/n (Default n) "
                )
            if not user_confirmation in ["y", "n"]:
                utils.warning("Invalid input. selectiong defult option")
                user_confirmation = "n"

            if not user_confirmation == "y":
                prefernce = False
                self._preference_modified = True
                user_data = {}
        else:
            prefernce = False

        token = user_data["token"] if "token" in user_data else None
        vaccine_type = user_data["vaccine_type"] if "vaccine_type" in user_data else None
        auto_book = user_data["auto_book"] if "auto_book" in user_data else None
        fee_type = user_data["fee_type"] if "fee_type" in user_data else None
        pincode = user_data["pincode"] if "pincode" in user_data else None
        district = user_data["district"] if "district" in user_data else None
        search_option = user_data["search_option"] if "search_option" in user_data else None
        search_freq = user_data["search_freq"] if "search_freq" in user_data else None
        
        if not token:
            if prefernce: utils.warning("Token not found in preferences")
            while not token:
                token = self.verify_mobile_number(mobile_number)
                self._preference_modified = True

        if not vaccine_type:
            if prefernce: utils.warning("Vaccine type not found in preferences")
            vaccine_type = utils.select_vaccine_type()
            self._preference_modified = True

        if not fee_type:
            if prefernce: utils.warning("Fee type not found in preferences")
            if input("Are you prefer free vaccine? y/n (Default n) ") == "y":
                fee_type = "free"
            else:
                fee_type = "paid"

            self._preference_modified = True

        if not search_freq:
            if prefernce: utils.warning("Search frequency not found in preferences")
            search_freq = input("How frequently you want search? (in sec) ")
            if search_freq.isnumeric():
                search_freq = int(search_freq)
            else:
                search_freq = 60

            self._preference_modified = True

        if not search_option:
            if prefernce: utils.warning("Search option not found in preferences")
            search_option = input("Seach by: \n\t1. District\t2. Pincode: (Default 2) ")
            if not search_option in ['1', '2']:
                utils.warning("Invalid search option. selecting default option")
                search_option = 2

            search_option = int(search_option)
            self._preference_modified = True

        if search_option == 1:
            search = SearchVaccineSlotesByDistricts()
            if not district:
                if prefernce: utils.warning("Preferred district not found")
                state = search.select_state()
                if state:
                    district = search.select_district(state)
                self._preference_modified = True

            search_param = district

        elif search_option == 2:
            search = SearchVaccineSlotesByPincode()
            if not pincode:
                if prefernce: utils.warning("Preferred pincode not found.")
                pincode = search.get_pincode()
                self._preference_modified = True

            search_param = pincode
            
        if not auto_book:
            if prefernce: utils.warning("Auto book option not enabled")
            if input("Do you want enable auto book option? y/n (Default n) ") == "y":
                auto_book = "y"
            else:
                auto_book = "n"

            self._preference_modified = True

        if self._preference_modified:
            if input("Do you want update preferences? y/n (Default n) ") == "y":
                self.user_data = {
                    "token" : token,
                    "auto_book" : auto_book,
                    "vaccine_type" : vaccine_type,
                    "fee_type" : fee_type,
                    "pincode" : pincode,
                    "district" : district,
                    "search_option" : search_option,
                    "search_freq" : search_freq
                }
                self.update_json(mobile_number, self.user_data)

        utils.message(
            "Search started with following parameters: \n\
            \tVaccine type: {} \n\
            \tFee type: {} \n\
            \tSearch option: {} \n\
            \tPincode: {} \n\
            \tDistrict: {} \n\
            \tSearch frequency: {}".format(
                vaccine_type, fee_type, search_option, pincode, 
                district, search_freq
            )
        )


        while True:
            result = search.get_vaccine_slots(search_param, vaccine_type)
            for item in result:
                if item["available_capacity"]:
                    utils.message("""Center: {}
Pincode: {}
Date: {}
Available Slots:{}
                        """.format(
                            item["center_name"], 
                            item["center_pincode"], 
                            item["date"], 
                            item["available_capacity"])
                            )
                else:
                    utils.flash_message(
                        "No vaccine at {} on {}".format(
                            item["center_name"], item["date"]
                            ), 0.01
                        )

            time.sleep(search_freq)
        
    def verify_mobile_number(self, mobile_number):
        """ 
        """
        try:
            response = self.authentication.generate_otp(mobile_number)
        except:
            response = 0

        if not response:
            utils.warning("{}: OTP request failed for {}".format(
                self.authentication.warning, mobile_number))
            return 0

        utils.message("Successfully requested OTP for {}".format(mobile_number))
        otp = sha256(str(input("Enter OTP: ")).encode("utf-8")).hexdigest()
        try:
            response = self.authentication.validate_otp(otp, response["txnId"])
        except:
            response = 0
        
        if not response:
            utils.warning("{}: OTP authentication failed.".format(self.authentication.utils.warning))
            return 0
        
        utils.message("Succesfull OTP verified.")
        return response["token"]



if __name__ == "__main__":
    try:
        co_vaccine_bot = CoVaccineBot()
        co_vaccine_bot.main()
    except KeyboardInterrupt:
        sys.exit()