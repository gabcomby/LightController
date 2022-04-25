import requests
#LIFX API TOKEN : c9a2305d2badf5dcf161325fc84c5a1249a9d8827fd4834e245b9dc8e51fce40

class LightController:
    def __init__(self):
        self.tokenAPI = "c9a2305d2badf5dcf161325fc84c5a1249a9d8827fd4834e245b9dc8e51fce40"
        self.headers = {"Authorization": "Bearer %s" % self.tokenAPI,}
        self.label = "LIFX Bulb"
        self.urlLumiere = 'https://api.lifx.com/v1/lights/label:' + self.label + '/state'

    def allumerAmpoule(self):
        payload = {"power": "on",
                   "color" : "white",}
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    def eteindreAmpoule(self):
        payload = {"power": "off",}
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    def easterEgg(self):
        payload = {"color": "red", }
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)