import requests
import json
'''
Objet qui va permettre de contrôler la lumière connectée LIFX à l'aide de requêtes HTTP vers le cloud de LIFX
(un serveur centralisé) qui envoie ensuite ces instructions à notre ampoule
'''
class LightController:
    def __init__(self):
        #Load l'API KEY et le Bulb Label sauvegardés dans le fichier SavedSettings.json
        with open('./SavedSettings.json', 'r') as f:
            self.donneesSauvegardees = json.load(f)
            f.close()
        self.tokenAPI = str(self.donneesSauvegardees['apiKey'])
        #Crée le header de chaque demande (ce qui authentifie notre identité auprès du serveur LIFX)
        self.headers = {"Authorization": "Bearer %s" % self.tokenAPI,}
        self.label = str(self.donneesSauvegardees['bulbLabel'])
        #Crée l'URL de la lumière afin de pouvoir indiquer au serveur LIFX sur quelle lumière connecter on veut agir
        self.urlLumiere = 'https://api.lifx.com/v1/lights/label:' + self.label + '/state'
        self.luminosite = 0.7

    '''
    Méthode pour allumer l'ampoule connectée
    '''
    def allumerAmpoule(self):
        #Crée un payload contenant toutes les instructions pour l'ampoule
        payload = {"power": "on",
                   "color" : "white",
                   "brightness" : self.luminosite, }
        #Envoie les instructions à l'ampoule (avec l'URL) en authentifiant que c'est bien nous (avec la clé d'API)
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    '''
    Méthode pour éteindre l'ampoule connectée
    '''
    def eteindreAmpoule(self):
        payload = {"power": "off",}
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    '''
    Méthode rigolote qui allume l'ampoule en rouge si on fait le signe "Call Me"
    '''
    def easterEgg(self):
        payload = {"color": "red", }
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)

    '''
    Méthode qui sauvegarde l'API KEY de l'utilisateur dans un fichier JSON pour les utilisations suivantes
    '''
    def changerApiKey(self, newApiKey):
        #Ouvre le fichier JSON en mode lecture, et lis les données qui y sont écrit
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        #Change la valeur de la clé d'API dans les données lues dans le JSON
        donnees['apiKey'] = newApiKey
        #Met à jour le header afin que l'application prenne le changement en compte directement (sans devoir redémarrer)
        self.headers = {"Authorization": "Bearer %s" % newApiKey,}
        #Écris la nouvelle valeur dans le fichier JSON afin de pouvoir la sauvegarder pour une prochaine utilisation
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()

    '''
    Méthode qui sauvegarde le Bulb Label de l'utilisateur dans un fichier JSON pour les utilisations suivantes
    '''
    def changerBulbLabel(self, newBulbLabel):
        with open('./SavedSettings.json', 'r') as f:
            donnees = json.load(f)
        donnees['bulbLabel'] = newBulbLabel
        self.urlLumiere = 'https://api.lifx.com/v1/lights/label:' + newBulbLabel + '/state'
        with open('./SavedSettings.json', 'w') as f:
            json.dump(donnees, f)
            f.close()

    '''
    Méthode qui change la luminosité de l'ampoule lorsque nous "pinçons" l'air. Augmente la luminosité si monterLuminosite
    est vrai, ne fait rien si monterLuminosite est null et la baisse si monterLuminosite est faux
    '''
    def changerLuminosité(self,monterLuminosite):
        #Tant que monterLuminosite est vrai, on augmente la luminosité de l'ampoule de 0.1 (jusqu'à un maximum de 1.0)
        if monterLuminosite :
            self.luminosite = self.luminosite + 0.1
            if self.luminosite > 1.0 :
                self.luminosite = 1.0
        #Tant que monterLuminosite est faux, on baisse la luminosité de l'ampoule de 0.1 (jusqu'à un maximum de 0.0)
        elif not monterLuminosite :
            self.luminosite = self.luminosite - 0.1
            if self.luminosite < 0:
                self.luminosite = 0
        #Envoie l'instruction de changer la luminosité à l'ampoule
        payload = {"brightness": self.luminosite, }
        response = requests.put(self.urlLumiere, data=payload, headers=self.headers)