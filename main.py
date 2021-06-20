from data import DATA
from view import VIEW

class MAIN(object):
    def __init__(self) -> None:
        super().__init__()
        self.name = "COWIN SEARCH SLOTS"
        self.data = DATA()
        self.view = VIEW()
    
    def run(self):
        result = self.data.get_api_data()
        self.view.show(result)

if "__main__" in __name__:
    main = MAIN()
    while True:
        main.run()
