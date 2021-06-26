import datetime
import requests
import os
import time


def _columnify(iterable):
    """ All elements padding with empty space in the list.
    args:
        iterable : list
    """
    widest = max(len(x) for x in iterable) + 1
    padded = [x.ljust(widest) for x in iterable]
    return padded

def column_print(iterable, width=os.get_terminal_size().columns):
    """ Printing elements column wise.
    args: 
        iterable : list
        width: int, optional
    """
    columns = _columnify(iterable)
    colwidth = len(columns[0])+2
    perline = (width-4) // colwidth
    print("", end='')
    for i, column in enumerate(columns):
        print(column, end="")
        if i % perline == perline-1:
            print("\n", end="")
    print("\n")

def warning(message):
    """ Print warning and error.
    args:
        message : str
    """
    print ("WARNING: {}".format(message), end="\n\n")

def message(message):
    """ Print message.
    args:
        messsage : str
    """
    print ("INFO: {}".format(message), end="\n\n")

def flash_message(message, duration=0):
    """ message overriding.
    args:
        message : str
        duration : int, time in second
    """
    print (message, end="\r")
    time.sleep(duration)
    print (" " * len(message), end="\r")

def get_today():
    """ Get today as %d-%m-%Y format.
    """
    today = datetime.date.today()
    return today.strftime("%d-%m-%Y")

def get_api_response(url, header):
    """ Utility function to get api response and handle exceptions
    args:
        url: str
        header: dict
    """
    response = requests.get( url, headers=header)

    if response.status_code == 200:
        return {"response" : response.json(), "warning": "Bad Request"}

    elif response.status_code == 400:
        return {"response" : 0, "warning": "Bad Request"}

    elif response.status_code == 401:
        return {"response" : 0, "warning": "Unauthenticated access"}

    elif response.status_code == 500:
        return {"response" : 0, "warning": "Internal Server Error"}

def select_vaccine_type():
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