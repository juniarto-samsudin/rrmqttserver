import requests

class MQTT_REST_API:
    def __init__(self):
        self.RestUrl = 'http://13.76.136.145:5005/api/mqtt'
        #self.RestUrl = 'http://127.0.0.1:5005/api/mqtt'
    def send(self, msgList):
        try:
            response = requests.post(self.RestUrl, json=msgList, timeout=5)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException, requests.exceptions.HTTPError, Exception) as err:
            print(err)
        else:
            print('OK')

