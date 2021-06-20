
import time

class CLI_VIEW(object):
    def read_search_by(self):
        search_by = input("Select search:\n\t1. State\n\t2. PINCODE\n")
        if not search_by in ["1", "2"]:
            print ("Invalid search")
            return 0
        return(int(search_by))

    def read_state_id(self, state_dict):
        for key in state_dict.keys():
            print ("{} : {}".format(state_dict[key], key))
        state_id = input("")
        if int(state_id) in state_dict.values():
            return int(state_id)
        else:
            print ("Invalid state")
            return 0

    def read_district_id(self, district_dict):
        for key in district_dict.keys():
            print ("{} : {}".format(district_dict[key], key))
        district_id = input("")
        if int(district_id) in district_dict.values():
            return int(district_id)
        else:
            print ("Invalid district")
            return 0


    def read_pincode(self):
        pincode = input("Enter the pincode:\n")
        return pincode

    def show(self, _data):
        for data in _data:
            for center in data['centers']:
                for session in center["sessions"]: 
                    if session["available_capacity"] > 0:
                        print ("Center : {} {}\n=======================".format(session['name'], session['pincode']))
                        print ("{} D1: {} D2: {} <<<<<<<<<<<<<".format(session["date"], session["available_capacity_dose1"], session["available_capacity_dose2"]))

