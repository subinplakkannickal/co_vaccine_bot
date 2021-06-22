import sys
import time
from utilities import column_print, flash_message, message, warning
from data.search_by_district import SearchByDistrict

class SearchVaccineSlotesByDistricts(object):
    def __init__(self, ):
        self.search_by_district_data = SearchByDistrict()

    def select_state(self):
        """ User interface for state seletion.
        """
        states = self.search_by_district_data.get_states()
        if not states:
            warning(self.search_by_district_data.warning)
            return 0
        
        # Display states list as table
        column_print(["{}: {}".format(id, states[id]) for id in states.keys()])

        # Reading user input
        state_id = input("Enter state id: ")

        # validate user input
        if state_id.isnumeric() and int(state_id) in states:
            message("State {} selected".format(states[int(state_id)]))
            return int(state_id)
        else:
            return 0

    def select_district(self, state_id):
        """ User interface for district selection.
        args:
            state_id : int
        """
        districts = self.search_by_district_data.get_districts(state_id)
        if not districts:
            warning(self.search_by_district_data.warning)
            return 0
        
        # Display districts list as table
        column_print(["{}: {}".format(id, districts[id]) for id in districts.keys()])

        # Reading user input
        district_id = input("Enter district id: ")

        # validate user input
        if district_id.isnumeric() and int(district_id) in districts:
            message("{} selected".format(districts[int(district_id)]))
            return int(district_id)
        else:
            return 0

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
        slots = self.search_by_district_data.get_api_data_by_district_id_for_7days(
            self.district_id, self.vaccine_type
            )
        if not slots:
            warning(self.search_by_district_data.warning)
            return 0

        # parsing search result
        result = []
        for center in slots["centers"]:
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

    def get_user_inputs(self):
        self.vaccine_type = self.select_vaccine_type()

        self.state_id = self.select_state()
        if not self.state_id: 
            warning("Invalid state selected")
            return 0


        self.district_id = self.select_district(self.state_id)
        if not self.district_id: 
            warning("Invalid district selected")
            return 0
        
        return 1


if __name__ == "__main__":
    try:
        main = SearchVaccineSlotesByDistricts()
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
                        flash_message("No vaccine at {}".format(item["center_name"]), 0.01)

                time.sleep(60)
    except KeyboardInterrupt:
        sys.exit()
