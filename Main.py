import Webcam as wc
import HandTracker as ht
import LightController as lc
import cv2
import time
from Main_GUI import *
from Settings_GUI import *
from PyQt5 import QtWidgets
import sys
#C:\Users\comby\AppData\Local\Programs\Python\Python38\Scripts\pyuic5 -x MainMenu.ui -o Main_GUI.py

lightController = lc.LightController()

def activerMain():
    global nomGeste
    nomGeste = "None"
    vieuxGeste = "NoneTest"
    webcam = wc.Webcam()
    handProcessor = ht.HandTrackProcessor()
    webcam.openWebcam()
    listeMarqueurs = []
    global timeStart
    timeStart = time.time()
    global timeFinish
    timeFinish = time.time()

    ####################################################################################################################
    #Méthode qui envoie chaque image capturée par OpenCV se faire calculer par HandController.py
    def calculsEtAnalyse(img, listeMarqueurs):
        global timeStart
        global timeFinish
        global nomGeste
        listeMarqueurs.clear()
        #On envoie l'image se faire analyser pour détecter les points de la main
        processedImage, listeMarqueurs = handProcessor.analyserImage(img)
        #On envoie UNIQUEMENT 1 image/seconde se faire analyser par l'algorithme TensorFlow de reconnaissance de mouvement
        #afin d'optimiser les performances du programme
        if timeFinish - timeStart >= 1:
            if(listeMarqueurs[0] != None):
                nomGeste = handProcessor.predictionGeste(listeMarqueurs)
            timeStart = timeFinish
        processedImage = cv2.flip(processedImage, 1)
        timeFinish = time.time()
        return processedImage
    ####################################################################################################################
    #Contrôle la lumière si le geste défini est détecté
    def controleDeLumière(lightController):
        global nomGeste
        if nomGeste == "fist":
            lightController.allumerAmpoule()
        elif nomGeste == "stop":
            lightController.eteindreAmpoule()
        elif nomGeste == "call me":
            lightController.easterEgg()
    #######################################################################################################################

    #Boucle de lecture infinie de la caméra
    while webcam.webcamIsOpen == True:
        frame = webcam.readWebcam()
        frame = calculsEtAnalyse(frame, listeMarqueurs)
        #Si le geste a changé depuis le précédent, on l'envoie au LightController
        if nomGeste != vieuxGeste and nomGeste != None:
            controleDeLumière(lightController)
            vieuxGeste = nomGeste
        cv2.imshow("Webcam", frame)
    webcam.closeWebcam()

#Code qui indique ce que font les boutons dans le menu principal du programme
class MainMenu(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.boutonDemarrer.clicked.connect(self.demarrer)
        self.boutonArret.clicked.connect(self.arreter)
        self.boutonParametre.clicked.connect(self.settingsMenu)
    #Bouton qui exécute tout le programme
    def demarrer(self):
        activerMain()
    #Bouton qui quitte le programme
    def arreter(self):
        lightController.eteindreAmpoule()
        sys.exit()
    #Bouton pour aller dans les settings
    def settingsMenu(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

#Code qui indique ce que font les boutons dans le menu des paramètres
class SettingsMenu(Ui_ParametersWindpw):
    def __init__(self, window):
        self.setupUi(window)
        self.BoutonApiKey.clicked.connect(self.apiSubmit)
        self.BoutonBulbLabel.clicked.connect(self.labelSubmit)
        self.BoutonRetourMenu.clicked.connect(self.retourMenu)
    #Bouton pour submit la nouvelle API KEY
    def apiSubmit(self):
        apiKey = self.ApiKeyTextBox.text()
        lightController.tokenAPI = apiKey
        lightController.changerApiKey(apiKey)
    #Bouton pour submit le nouveau Bulb Label
    def labelSubmit(self):
        bulbLabel = self.BulbLabelTextBox.text()
        lightController.label = bulbLabel
        lightController.changerBulbLabel(bulbLabel)
    #Bouton pour retourner au menu principal
    def retourMenu(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


#Code pour afficher le GUI
app = QtWidgets.QApplication(sys.argv)
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