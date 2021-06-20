import time
from data import DATA
from view import CLI_VIEW

class MAIN(object):
    def __init__(self) -> None:
        super().__init__()
        self.name = "COWIN SEARCH SLOTS"
        self.data = DATA()
        self.view = CLI_VIEW()
    
    def get_user_input(self):
        self.search_by = self.view.read_search_by()
        if self.search_by == 1:
            state_dict = self.data.get_states()
            state_id = self.view.read_state_id(state_dict)
            if state_id == 0:
                return 0

            district_dict = self.data.get_districts(state_id)
            self.district_id = self.view.read_district_id(district_dict)
            if self.district_id == 0:
                return 0
            return 1

        elif self.search_by == 2:
            self.pincode = self.view.read_pincode()
            return 1

    def run(self):
        while True:
            if self.search_by == 1:
                result = self.data.get_api_data_by_district_id_for_7days(self.district_id)

            elif self.search_by == 2:
                result = self.data.get_api_data_by_pincode_for_7days(self.pincode)

            self.view.show(result)
            time.sleep(5)

if "__main__" in __name__:
    main = MAIN()
    if main.get_user_input():
        main.run()
