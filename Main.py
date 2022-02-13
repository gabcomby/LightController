import Webcam as wc
import HandTracker as ht
import cv2
import time

print("╔═══════════════════════╗")
print(" HandController V. 0.1.0")
print("╚═══════════════════════╝")
tempsActuel, tempsPrecedent = 0, 0
webcam = wc.Webcam()
handProcessor = ht.HandTrackProcessor()
webcam.openWebcam()

########################################################################################################################
def calculsEtAnalyse(img, tempsPrecedent):
    processedImage = handProcessor.analyserImage(frame)  #On envoie l'image se faire analyser dans le HandTracker
    listeMarqueurs = handProcessor.positionMain(frame)
    print(listeMarqueurs)
    processedImage = cv2.flip(processedImage, 1)
    tempsActuel = time.time()
    fps = 1 / (tempsActuel - tempsPrecedent)  #Calcul du framerate de la webcam
    tempsPrecedent = tempsActuel
    processedImage = cv2.putText(processedImage, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 255), 3)
    return processedImage, tempsPrecedent
########################################################################################################################

while webcam.webcamIsOpen == True:
    frame =webcam.readWebcam()
    processedImage, tempsPrecedent = calculsEtAnalyse(frame, tempsPrecedent)
    cv2.imshow("Webcam", processedImage)
    cv2.setWindowProperty("Webcam", cv2.WND_PROP_TOPMOST, 1)
webcam.closeWebcam