import datetime

def get_today():
    """ Get today as %d-%m-%Y format.
    """
    today = datetime.date.today()
    return today.strftime("%d-%m-%Y")