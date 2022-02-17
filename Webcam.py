import cv2
import HandTracker as ht
import time

class Webcam :
    def __init__(self):
        self.closeWebcam = None
        self.indexWebcam = 0
        self.webcamIsOpen = False
        self.widthWebcam = 640
        self.heightWebcam = 480
        self.nomFenetre = "Webcam"
        self.cam = None
        self.tempsActuel = 0
        self.tempsPrecedent = 0
        self.handProcessor = ht.HandTrackProcessor()

    def openWebcam(self): #Ouvre la webcam et set ses dimentions
        self.webcamIsOpen = True
        self.cam = cv2.VideoCapture(self.indexWebcam)
        self.cam.set(3, self.widthWebcam)
        self.cam.set(4, self.heightWebcam)

    def readWebcam(self): #Retourne une image de la webcam
        ret, frame = self.cam.read()
        cv2.waitKey(1)
        #Si on appuie sur ESC ça sort de la boucle infinie
        if cv2.waitKey(1) == 27:
            self.webcamIsOpen = False
        return frame

    def closeWebcam(self): #Ferme la webcam et le programme
        cv2.destroyAllWindows
        self.cam.release