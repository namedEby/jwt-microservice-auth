import requests

class ServiceHandler():

    service_a = "https://127.0.0.1:8080/tokens/"
    service_b = "https://127.0.0.1:8090/tokens/"

    def __init__(self, params):
        try:
            getattr(self, self.params.service.upper())()
        except AttributeError:
            self.response = "Invalid Service Name"
            self.response_code = 400

