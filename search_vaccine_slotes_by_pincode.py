import sys
import time
from utils.utils import (
    flash_message, get_api_response, message, warning, select_vaccine_type
    )
from abstract_slot_search import AbstractSlotSearch
from data.search_by_pincode import SearchByPincode

class SearchVaccineSlotesByPincode(AbstractSlotSearch):
    def __init__(self, ):
        self.search_by_pincode_data = SearchByPincode()

    def get_vaccine_slots(self, pincode, vaccine_type):
        slots = [self.search_by_pincode_data.get_api_data_by_pincode_for_7days(
            _pincode, self.vaccine_type
            ) for _pincode in pincode]

        if not slots:
            warning(self.search_by_pincode_data.warning)
            return 0

        # parsing search result
        result = []
        for slot in slots:
            for center in slot["centers"]:
                for session in center["sessions"]:
                    result.append(
                        {
                            "center_name" : center["name"],
                            "center_id" : center["center_id"],
                            "center_pincode" : center["pincode"],
                            "fee_type" : center["fee_type"],
                            "date" : session["date"],
                            "available_capacity" : session["available_capacity"],
                            "available_capacity_dose1" : session["available_capacity_dose1"],
                            "available_capacity_dose2" : session["available_capacity_dose2"],
                            "age_limit" : session["min_age_limit"],
                            "slots" : session["slots"] if session["available_capacity"] > 0 else []
                        }
                    )

        return result

    def get_pincode(self):
        """ User interfce to get pincode.
        """
        pincode_list = []
        pincode = input("Enter pincode: ")
        while True:
            if pincode.isnumeric and len(pincode) == 6:
                pincode_list.append(pincode)
            else:
                warning("invalid pincode")

            pincode = input(
                "Do you want search for more pincode? Enter pincode if yes else n (Default n) "
                )
            if not pincode or pincode == 'n':
                break

        message("Selected pincodes: {}".format(", ".join(pincode_list)))

        return pincode_list

    def get_user_inputs(self, vaccine_type=None, pincode=None):
        """ Get user input for select pincode
        args:
            vaccine_type: str, optional
            pincode: list, optional
        """
        if not vaccine_type:
            vaccine_type = select_vaccine_type()

        if not pincode:
            pincode = self.get_pincode()

        if not pincode:
            warning("Invalid pincode selected")
        
        return pincode, vaccine_type


if __name__ == "__main__":
    try:
        main = SearchVaccineSlotesByPincode()
        pincode, vaccine_type = main.get_user_inputs()
        if pincode and vaccine_type:
            while True:
                result = main.get_vaccine_slots(pincode, vaccine_type)
                for item in result:
                    if item["available_capacity"]:
                        message("""Center: {}
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
                        flash_message("No vaccine at {} on {}".format(item["center_name"], item["date"]), 0.01)

                time.sleep(60)
    except KeyboardInterrupt:
        sys.exit()
