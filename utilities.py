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
        width: int 
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
