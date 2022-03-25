import Webcam as wc
import HandTracker as ht
import LightController as lc
import cv2
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

print("╔═══════════════════════╗")
print(" HandController V. 0.5.0")
print("╚═══════════════════════╝")
global nomGeste
nomGeste = "None"
vieuxGeste = "NoneTest"
webcam = wc.Webcam()
handProcessor = ht.HandTrackProcessor()
lightController = lc.LightController()
webcam.openWebcam()
listeMarqueurs = []
global timeStart
timeStart = time.time()
global timeFinish
timeFinish = time.time()

########################################################################################################################
def calculsEtAnalyse(img, listeMarqueurs):
    global timeStart
    global timeFinish
    global nomGeste
    listeMarqueurs.clear()
    processedImage, listeMarqueurs = handProcessor.analyserImage(img)  #On envoie l'image se faire analyser dans le HandTracker
    if timeFinish - timeStart >= 1:
        if(listeMarqueurs[0] != None):
            nomGeste = handProcessor.predictionGeste(listeMarqueurs)
        timeStart = timeFinish
    processedImage = cv2.flip(processedImage, 1)
    timeFinish = time.time()
    return processedImage
########################################################################################################################

def controleDeLumière(lightController):
    global nomGeste
    if nomGeste == "fist":
        lightController.allumerAmpoule()
    elif nomGeste == "stop":
        lightController.eteindreAmpoule()
    elif nomGeste == "call me":
        lightController.easterEgg()


while webcam.webcamIsOpen == True:
    frame = webcam.readWebcam()
    frame = calculsEtAnalyse(frame, listeMarqueurs)
    if nomGeste != vieuxGeste and nomGeste != None:
        print(nomGeste)
        controleDeLumière(lightController)
        vieuxGeste = nomGeste
    cv2.imshow("Webcam", frame)
webcam.closeWebcam
lightController.eteindreAmpoule()