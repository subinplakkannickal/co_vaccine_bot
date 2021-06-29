import sys
import time
from utils.utils import (column_print, 
    flash_message, message, warning, select_vaccine_type
    )
from abstract_slot_search import AbstractSlotSearch
from data.search_by_district import SearchByDistrict


class SearchVaccineSlotesByDistricts(AbstractSlotSearch):
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

    def get_vaccine_slots(self, district_id, vaccine_type):
        """
        """
        slots = self.search_by_district_data.get_api_data_by_district_id_for_7days(
            district_id, vaccine_type
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

    def get_user_inputs(self, vaccine_type=None, district=None):
        """ Get user input for select state and district.
        args:
            vaccine_type : str, optional
            district: int, optional
        """
        if vaccine_type:
            vaccine_type = select_vaccine_type()

        if not district:
            state_id = self.select_state()
            if not state_id: 
                warning("Invalid state selected")
                return 0, vaccine_type

            district_id = self.select_district(self.state_id)
            if not district_id: 
                warning("Invalid district selected")
                return 0, vaccine_type
        
        return district_id, vaccine_type


if __name__ == "__main__":
    try:
        main = SearchVaccineSlotesByDistricts()
        district_id, vaccine_type = main.get_user_inputs()
        if district_id and vaccine_type:
            while True:
                result = main.get_vaccine_slots(district_id, vaccine_type)
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
