import Webcam as wc
import HandTracker as ht
import LightController as lc
import cv2
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

print("╔═══════════════════════╗")
print(" HandController V. 0.3.0")
print("╚═══════════════════════╝")
webcam = wc.Webcam()
handProcessor = ht.HandTrackProcessor()
lightController = lc.LightController()
lightController.allumerAmpoule()
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
    listeMarqueurs.clear()
    processedImage, listeMarqueurs = handProcessor.analyserImage(img)  #On envoie l'image se faire analyser dans le HandTracker
    if timeFinish - timeStart >= 1:
        if(listeMarqueurs[0] != None):
            handProcessor.predictionGeste(listeMarqueurs)
        timeStart = timeFinish
    processedImage = cv2.flip(processedImage, 1)
    timeFinish = time.time()
    return processedImage
########################################################################################################################

while webcam.webcamIsOpen == True:
    frame = webcam.readWebcam()
    frame= calculsEtAnalyse(frame, listeMarqueurs)
    cv2.imshow("Webcam", frame)
webcam.closeWebcam
lightController.eteindreAmpoule()