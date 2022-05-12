import Webcam as wc
import HandTracker as ht
import LightController as lc
import cv2
import time
from Main_GUI import *
from Settings_GUI import *
from PyQt5 import QtWidgets
import sys

lightController = lc.LightController()


def activerMain():
    #Variable qui stocke le nom du geste détecté par le modèle TensorFlow
    global nomGeste
    nomGeste = "None"
    vieuxGeste = "NoneTest"
    #Crée les objets pour la webcam, l'analyse de la main et le contrôle de la lumière
    webcam = wc.Webcam()
    handProcessor = ht.HandTrackProcessor()
    webcam.openWebcam()
    listeMarqueurs = []
    #Initialise le temps de début du programme (utilisé plus tard dans le Main)
    global timeStart
    timeStart = time.time()
    #Intialise une seconde variable de temps (utilisé plus tard dans le Main)
    global timeFinish
    timeFinish = time.time()
    #Active le mode de contrôle de la lumière par les gestes par défaut (plutôt que le mode de contrôle de la luminosité)
    global calculerGeste
    calculerGeste = True
    #Distance initiale entre les deux doigts pour le contrôle de la luminosité
    global derniereDistance
    derniereDistance = 10000

    '''
    Méthode qui calcule la distance entre le pouce et l'index dans l'image et la retourne, utilisée lorsque l'on veut
    changer la luminosité avec les doigts
    '''
    def calculerDistancePouceIndex(positionIndex, positionPouce, listeMarqueurs):
        distancePouceIndex = 100
        #Si le programme détecte une main, alors il va calculer la distance pouce-index
        if (len(listeMarqueurs) != 0) and (listeMarqueurs[0] != None):
            #Coordonnées du point du pouce
            posIndexX, posIndexY = positionIndex[0], positionIndex[1]
            #Coordonnées du point de l'index
            posPouceX, posPouceY = positionPouce[0], positionPouce[1]
            #Calcule la distance entre les deux points
            distancePouceIndex = ((posPouceX - posIndexX) ** 2) + ((posPouceY - posIndexY) ** 2)
        return distancePouceIndex

    '''
    Vérifie si la distance pouce index a augmenté ou diminué depuis la dernière fois, et retourne un boolean en fonction
    de si ça a augmenté ou baissé
    '''
    def variationDistance(derniereDistance, distance):
        distanceAugmente = None
        #Calcul la différence de distance entre la dernière distance et la nouvelle
        deltaDistance = distance-derniereDistance
        #Si la distance a augmentée ou diminuée de 25px ou plus, alors on set la valeur du booléen distanceAugmente
        if  deltaDistance >= 25:
            distanceAugmente = True
        elif deltaDistance <= -25:
            distanceAugmente = False
        return distanceAugmente

    '''
    Méthode qui envoie chaque image capturée par OpenCV être analysée par les deux méthodes de HandController.py
    (suivi de la main avec Mediapipe et reconnaissance de gestes avec TensorFlow). Prend aussi en charge le "mode
    luminosité", qui désactive la reconnaissance de geste et active le calcul de distance pouce-index.
    '''
    def calculsEtAnalyse(img, listeMarqueurs):
        #Importe les variables globales
        global timeStart
        global timeFinish
        global nomGeste
        global derniereDistance
        global calculerGeste #Ici
        distanceAugmente = None
        #On clear la liste de marqueurs
        listeMarqueurs.clear()
        #On envoie l'image se faire analyser par Mediapipe pour détecter la main et obtenir les coordonnées des 21
        #points
        processedImage, listeMarqueurs = handProcessor.analyserImage(img)
        #On note les coordonnées des points du pouce et de l'index
        positionIndex = listeMarqueurs[8]
        positionPouce = listeMarqueurs[4]
        #Si le mode "Geste" est activé, alors on envoie 1 image/seconde se faire analyser par le modèle TensorFlow
        #afin d'y détecter les gestes effectués (1 image/seconde afin d'améliorer les performances)
        if calculerGeste:
            #Vérifie qu'on envoie 1 image par seconde
            if timeFinish - timeStart >= 1:
                #Si le programme détecte une main, alors on l'envoie se faire analyser par le modèle TensorFlow
                if(listeMarqueurs[0] != None):
                    nomGeste = handProcessor.predictionGeste(listeMarqueurs)
                    #Calcule la distance pouce-index pour avoir une valeur de référence
                    derniereDistance = calculerDistancePouceIndex(positionIndex, positionPouce, listeMarqueurs)
                #Note le temps de début de l'opération
                timeStart = timeFinish
        #Note le temps actuel
        timeFinish = time.time()
        #Si l'utilisateur active le mode "Luminosité", alors on n'envoie plus de données au modèle TensorFlow, on analyse
        #seulement la distance pouce-index pour modifier la luminosité
        if not calculerGeste:
            #Calcule la distance pouce index
            distance = calculerDistancePouceIndex(positionIndex, positionPouce, listeMarqueurs)
            #Vérifie si la distance a augmenté ou réduit depuis la dernière mesure
            distanceAugmente = variationDistance(derniereDistance, distance)
            #Change la luminosité de l'objet lightController en fonction du boolean distanceAugmente
            lightController.changerLuminosité(distanceAugmente)
            #Note la dernière distance
            derniereDistance = distance
            #Note le temps actuel
            timeFinish = time.time()
            #Calcule 10 secondes puis désactive automatiquement le mode "Luminosité"
            if timeFinish - timeStart >= 10:
                calculerGeste = True
        #Tourne l'image pour une vue de type "mirroir"
        processedImage = cv2.flip(processedImage, 1)
        return processedImage

    '''
    Contrôle la lumière si le geste défini est détecté
    '''
    def controleDeLumière(lightController):
        global nomGeste
        if nomGeste == "fist":
            lightController.allumerAmpoule()
        elif nomGeste == "stop":
            lightController.eteindreAmpoule()
        elif nomGeste == "call me":
            lightController.easterEgg()

    '''
    Boucle de lecture infinie de la caméra
    '''
    while webcam.webcamIsOpen == True:
        #Lis une image depuis la webcam
        frame = webcam.readWebcam()
        #Envoie cette image à la méthode calculsEtAnalyse (voir plus haut)
        frame = calculsEtAnalyse(frame, listeMarqueurs)
        #Si le geste a changé depuis le précédent, on l'envoie au LightController
        if nomGeste != vieuxGeste and nomGeste != None:
            controleDeLumière(lightController)
            #On note le geste afin d'éviter le spam d'instructions identiques
            vieuxGeste = nomGeste
        #Affiche l'image à l'écran
        cv2.imshow("Webcam", frame)
    webcam.closeWebcam()

'''
Code qui définit ce que font chacun des boutons dans la fenêtre du menu principal
'''
class MainMenu(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.boutonDemarrer.clicked.connect(self.demarrer)
        self.boutonArret.clicked.connect(self.arreter)
        self.boutonParametre.clicked.connect(self.settingsMenu)
        self.boutonLuminosite.clicked.connect(self.modeLuminosite)
    #Bouton qui lance le programme en mode "Gestes"
    def demarrer(self):
        activerMain()
    #Bouton qui quitte le programme
    def arreter(self):
        lightController.eteindreAmpoule()
        sys.exit()
    #Bouton pour aller dans le menu des paramètres
    def settingsMenu(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    #Bouton qui active le mode "Luminosité"
    def modeLuminosite(self):
        global calculerGeste
        global timeStart
        calculerGeste = False
        #Note le début du mode "Luminosité" afin que ce dernier dure exactement 10 secondes
        timeStart = time.time()

'''
Code qui définit ce que font chacun des boutons dans la fenêtre du menu des paramètres
'''
class SettingsMenu(Ui_ParametersWindpw):
    def __init__(self, window):
        self.setupUi(window)
        self.BoutonApiKey.clicked.connect(self.apiSubmit)
        self.BoutonBulbLabel.clicked.connect(self.labelSubmit)
        self.BoutonRetourMenu.clicked.connect(self.retourMenu)
    #Bouton pour submit la nouvelle API KEY
    def apiSubmit(self):
        #On prend le texte qui était dans le Text Box
        apiKey = self.ApiKeyTextBox.text()
        #On change la clé d'API à l'aide d'une méthode de LightController
        lightController.changerApiKey(apiKey)
    #Bouton pour submit le nouveau Bulb Label
    def labelSubmit(self):
        #On prend le texte qui était dans le Text Box
        bulbLabel = self.BulbLabelTextBox.text()
        #On change le bulb label à l'aide d'une méthode de LightController
        lightController.changerBulbLabel(bulbLabel)
    #Bouton pour retourner au menu principal
    def retourMenu(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


#Code pour afficher le GUI
app = QtWidgets.QApplication(sys.argv)
#Widget empilé dans lequel on place nos deux fenêtres de menu afin de pouvoir facilement passer de l'une à l'autre
widget = QtWidgets.QStackedWidget()
MainWindow = QtWidgets.QMainWindow()
SettingsWindow = QtWidgets.QMainWindow()
ui = MainMenu(MainWindow)
ui2 = SettingsMenu(SettingsWindow)
widget.addWidget(MainWindow)
widget.addWidget(SettingsWindow)
widget.setFixedWidth(960)
widget.setFixedHeight(540)
widget.show()
app.exec_()