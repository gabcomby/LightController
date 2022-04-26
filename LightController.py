import requests
import json
#LIFX API TOKEN : c9a2305d2badf5dcf161325fc84c5a1249a9d8827fd4834e245b9dc8e51fce40
#LIFX Bulb Token : LIFX Bulb

class LightController:
    def __init__(self):
        with open('./SavedSettings.json', 'r') as f:
            self.donneesSauvegardees = json.load(f)
            f.close()
        self.tokenAPI = str(self.donneesSauvegardees['apiKey'])
        self.headers = {"Authorization": "Bearer %s" % self.tokenAPI,}
        self.label = str(self.donneesSauvegardees['bulbLabel'])
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

    def changerApiKey(self, newApiKey):
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        donnees['apiKey'] = newApiKey
        self.headers = {"Authorization": "Bearer %s" % newApiKey,}
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()

    def changerBulbLabel(self, newBulbLabel):
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        donnees['bulbLabel'] = newBulbLabel
        self.urlLumiere = 'https://api.lifx.com/v1/lights/label:' + newBulbLabel + '/state'
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()