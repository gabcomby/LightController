import Webcam as wc
import HandTracker as ht
import cv2
import numpy as np

print("╔═══════════════════════╗")
print(" HandController V. 0.3.0")
print("╚═══════════════════════╝")
webcam = wc.Webcam()
handProcessor = ht.HandTrackProcessor()
webcam.openWebcam()
listeMarqueurs = []

########################################################################################################################
def calculsEtAnalyse(img, listeMarqueurs):
    listeMarqueurs.clear()
    processedImage, listeMarqueurs = handProcessor.analyserImage(img)  #On envoie l'image se faire analyser dans le HandTracker
    if(listeMarqueurs[0] != None):
        handProcessor.predictionGeste(listeMarqueurs)
    processedImage = cv2.flip(processedImage, 1)
    return processedImage
########################################################################################################################

while webcam.webcamIsOpen == True:
    frame =webcam.readWebcam()
    processedImage = calculsEtAnalyse(frame, listeMarqueurs)
    #processedImage = cv2.putText(processedImage, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 255), 3)
    cv2.imshow("Webcam", processedImage)
webcam.closeWebcam