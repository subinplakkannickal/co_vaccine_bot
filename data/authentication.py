from utilities import message
import requests
from utils import url

class Authentication(object):
    def __init__(self):
        self._generate_otp_url = url.GENERATE_OTP_URL
        self._header = url.HEADER

    def generate_otp(self, mobile_number):
        """ Function to generate otp for given mobile number.
        args:
            mobile_number: int
        """
        data = {
                "mobile": mobile_number
            }
        response = requests.post(url=self._generate_otp_url, json=data, headers=self._header)

        if response.status_code == 200:
            message(response)
            return response.json()

        elif response.status_code == 400:
            self.warning = "Bad Request"
            return 0

        elif response.status_code == 401:
            self.warning = "Unauthenticated access"
            return 0

        elif response.status_code == 500:
            self.warning = "Internal Server Error"
            return 0

    def validate_otp(self, otp, txn_id):
        """ OTP Validator.
        args:
            otp: sha256 hash
            txn_id: transaction id
        """
        data = {
                "otp": otp,
                "txnId": txn_id,
            }
        response = requests.post(
                        url=url.VALIDATE_OTP_URL, json=data, headers=url.HEADER,
                    )
        if response.status_code == 200:
            return response.json()

        elif response.status_code == 400:
            self.warning = "Bad Request"
            return 0

        elif response.status_code == 401:
            self.warning = "Unauthenticated access"
            return 0

        elif response.status_code == 500:
            self.warning = "Internal Server Error"
            return 0