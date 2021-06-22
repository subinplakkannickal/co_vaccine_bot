import sys
import time
from utilities import column_print, flash_message, message, warning
from data.search_by_pincode import SearchByPincode

class SearchVaccineSlotesByPincode(object):
    def __init__(self, ):
        self.search_by_pincode_data = SearchByPincode()

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

    def get_vaccine_slots(self):
        slots = [self.search_by_pincode_data.get_api_data_by_pincode_for_7days(
            pincode, self.vaccine_type
            ) for pincode in self.pincode]
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
        while True:
            pincode = input("Enter pincode: ")
            if pincode.isnumeric and len(pincode) == 6:
                pincode_list.append(pincode)
            else:
                warning("invalid pincode")

            if not input("Do you want search for more pincode? y/n ") == 'y':
                break

        message("Selected pincodes: {}".format(", ".join(pincode_list)))

        return pincode_list

    def get_user_inputs(self):
        self.vaccine_type = self.select_vaccine_type()

        self.pincode = self.get_pincode()
        if not self.pincode: 
            warning("No pincode selected")
            return 0
        
        return 1


if __name__ == "__main__":
    try:
        main = SearchVaccineSlotesByPincode()
        if main.get_user_inputs():
            while True:
                result = main.get_vaccine_slots()
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
