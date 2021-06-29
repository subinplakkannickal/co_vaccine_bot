import sys
import os
import json
from copy import deepcopy
from hashlib import sha256
from utils import utils
from data.authentication import Authentication
from search_vaccine_slotes_by_districts import SearchVaccineSlotesByDistricts
from search_vaccine_slotes_by_pincode import SearchVaccineSlotesByPincode

class CoVaccineBot(object):
    def __init__(self):
        self.authentication = Authentication()
        self.user_data = {
            "token" : None,
            "auto_book" : False,
            "vaccine_type" : None,
            "fee_type" : 0,
            "pincode" : [],
            "state" : 0,
            "district" : 0,
            "search_option" : 2
        }

    def read_json(self, mobile_number):
        """ Read user json file from /home/${user}/tmp/co_vaccine_bot/
        args:
            mobile_number: int
        """
        file_name = "/home/{}/tmp/co_vaccine_bot/{}.json".format(os.getlogin(), mobile_number)
        if not os.path.exists(file_name):
            return 0

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

        utils.message("{} updated with {}".format(file_name, data))
        
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
            user_confirmation = input(
                "User preference found. Do you continue with previous preference? y/n (Default n) "
                )

            if not user_confirmation in ["y", "n"]:
                utils.warning("Invalid input. selectiong defult option")
                user_confirmation = "n"
            
            if not user_confirmation == "y":
                user_data = deepcopy(self.user_data)
            
            else:
                self.user_data = user_data

        else:
            user_data = deepcopy(self.user_data)

        token = user_data["token"]
        vaccine_type = user_data["vaccine_type"]
        auto_book = user_data["auto_book"]
        fee_type = user_data["fee_type"]
        pincode = user_data["pincode"]
        state = user_data["state"]
        district = user_data["district"]
        search_option = user_data["search_option"]
        
        if not token:
            utils.warning("Token not found in preferences")
            token = self.verify_mobile_number(mobile_number)
            self.user_data["token"] = token

        if not vaccine_type:
            utils.warning("Vaccine type not found in preferences")
            vaccine_type = utils.select_vaccine_type()
            self.user_data["vaccine_type"] = vaccine_type

        if not search_option:
            utils.warning("Search option not found in preferences")
            search_option = input("Seach by: \n\t1. PINCODE\t2. District: (Default 2) ")
            if not search_option in ['1', '2']:
                utils.warning("Invalid search option. selecting default option")
                search_option = 2

            self.user_data["search_option"] = int(search_option)

        if search_option == 1:
            self.search = SearchVaccineSlotesByDistricts()
        else:
            self.search = SearchVaccineSlotesByPincode()

        if search_option == 1 and not district:
            utils.warning("Preferred district not found")
            

        elif search_option == 2 and not pincode:
            utils.warning("Preferred pincode not found.")
            pincode = self.search.get_pincode()
            self.user_data["pincode"] = pincode
            

        if not self.user_data == user_data:
            if input("Do you want update preferences? y/n (Default n) ") == "y":
                self.update_json(mobile_number, self.user_data)

        

    def verify_mobile_number(self, mobile_number):
        """ 
        """
        try:
            response = self.authentication.generate_otp(mobile_number)
        except:
            response = 0

        if not response:
            utils.warning("{}: OTP request failed for {}".format(
                self.authentication.utils.warning, mobile_number))
            return 0

        utils.message("Successfully requested OTP for {}".format(mobile_number))
        otp = sha256(str(input("Enter OTP: ")).encode("utf-8")).hexdigest()
        utils.message(otp)

        try:
            response = self.authentication.validate_otp(otp, response["txnId"])
            utils.message(response)
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