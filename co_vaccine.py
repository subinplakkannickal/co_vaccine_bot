import sys
import os
import json
from hashlib import sha256
from utilities import message, warning, column_print
from data.authentication import Authentication
from search_vaccine_slotes_by_districts import SearchByDistrict
from search_vaccine_slotes_by_pincode import SearchByPincode

class CoVaccineBot(object):
    def __init__(self):
        self.authentication = Authentication()
        self.user_data = {
            "mobile_number" : "",
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
        

    def main(self):
        message("CO VACCINE BOT started")
        # Get user inputs
        while True:
            mobile_number = input("Enter registered mobile number: ")
            if len(mobile_number) == 10 and mobile_number.isnumeric():
                break
            else:
                warning("Invalid mobile number")
                if not input("Do you want contineue? y/n ") == "y":
                    break
        
        user_data = self.read_json(mobile_number)
        user_confirmation = input(
            "User preference found. Do you continue with previous preference? y/n (Default n) "
            )
        
        if user_confirmation == "y":
            token = user_data["token"]
            vaccine_type = user_data["vaccine_type"]
            auto_book = user_data["auto_book"]
            fee_type = user_data["fee_type"]
            pincode = user_data["pincode"]
            state = user_data["state"]
            district = user_data["district"]
            search_option = user_data["search_option"]
        
        if not token:
            warning("Token not found")
            token = self.verify_mobile_number(mobile_number)
            self.user_data["token"] = token

        if not vaccine_type:
            warning("Vaccine type not found")
            token = self.verify_mobile_number(mobile_number)
            self.user_data["token"] = token
        

        if not token:
            return 0

        

        message("Token generated for {}: {}".format(mobile_number, token))
        # self.update_json(mobile_number)
        search_option = input("Seach by \n\t1. PINCODE\t2. District")

    def verify_mobile_number(self, mobile_number):
        """ 
        """
        response = self.authentication.generate_otp(mobile_number)
        if not response:
            warning("{}: OTP request failed for {}".format(
                self.authentication.warning, mobile_number))
            return 0

        message("Successfully requested OTP for {}".format(mobile_number))
        otp = sha256(str(input("Enter OTP: ")).encode("utf-8")).hexdigest()
        message(otp)

        response = self.authentication.validate_otp(otp, response["txnId"])
        message(response)
        if not response:
            warning("{}: OTP authentication failed.".format(self.authentication.warning))
            return 0
        
        message("Succesfull OTP verified.")
        return response["token"]

    def select_vaccine_type(self):
        """ User interface for vaccine type.
        """
        available_vaccine_types = {1 : "COVISHIELD", 2 : "COVAXINE", 3 : "SPUTNIK V"}

        # Display vaccne type list as table
        column_print(["{}: {}".format(id, available_vaccine_types[id]) for id in available_vaccine_types.keys()])

        vaccine_type = input("Enter vaccine type: ")

        # validate user input
        if vaccine_type.isnumeric() and int(vaccine_type) in available_vaccine_types:
            message("Vaccine type {} selected".format(available_vaccine_types[int(vaccine_type)]))
            return available_vaccine_types[int(vaccine_type)]
        else:
            message("{} selected".format(available_vaccine_types[1]))
            return available_vaccine_types[1]


if __name__ == "__main__":
    try:
        co_vaccine_bot = CoVaccineBot()
        co_vaccine_bot.main()
    except KeyboardInterrupt:
        sys.exit()