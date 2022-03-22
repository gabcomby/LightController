import requests

class LightController:
    def __init__(self):
        self.tokenAPI = "c9a2305d2badf5dcf161325fc84c5a1249a9d8827fd4834e245b9dc8e51fce40"
        self.headers = {"Authorization": "Bearer %s" % self.tokenAPI,}

    def allumerAmpoule(self):
        payload = {"power": "on",}
        response = requests.put('https://api.lifx.com/v1/lights/label:LIFX Bulb/state', data=payload, headers=self.headers)

    def eteindreAmpoule(self):
        payload = {"power": "off",}
        response = requests.put('https://api.lifx.com/v1/lights/label:LIFX Bulb/state', data=payload, headers=self.headers)