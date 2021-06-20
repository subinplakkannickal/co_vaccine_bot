
import time

class VIEW(object):
    def show(self, data):
        for data_item in data:
            for session in data_item['sessions']:
                if session["available_capacity"] > 0: 
                    print ("{} : {} :\t{} <<<<<".format(session["date"], session["name"], session["available_capacity"]))
                else:
                    print ("{} : {} :\t{}".format(session["date"], session["name"], session["available_capacity"]))
                time.sleep(3)
