import requests
import json
#LIFX API TOKEN : c9a2305d2badf5dcf161325fc84c5a1249a9d8827fd4834e245b9dc8e51fce40
#LIFX Bulb Token : LIFX Bulb

#Objet qui contrôle la lumière connectée LIFX
class LightController:
    def __init__(self):
        #Load l'API KEY et le Bulb Label depuis un fichier JSON
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

    #Petite méthode blague qui allume la lumière en rouge
    def easterEgg(self):
        payload = {"color": "red", }
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    #Méthode qui sauvegarde l'API KEY de l'utilisateur dans un fichier JSON pour les utilisations suivantes
    def changerApiKey(self, newApiKey):
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        donnees['apiKey'] = newApiKey
        self.headers = {"Authorization": "Bearer %s" % newApiKey,}
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()

    #Méthode qui sauvegarde le Bulb Label de l'utilisateur dans un fichier JSON pour les utilisations suivantes
    def changerBulbLabel(self, newBulbLabel):
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        donnees['bulbLabel'] = newBulbLabel
        self.urlLumiere = 'https://api.lifx.com/v1/lights/label:' + newBulbLabel + '/state'
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()