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

    def openWebcam(self):
        webcamIsOpen = True
        cam = cv2.VideoCapture(self.indexWebcam)  #Ouvre la webcam
        cam.set(3, self.widthWebcam)
        cam.set(4, self.heightWebcam)
        while True:  #Boucle infinie
            ret, frame = cam.read()
            processedImage = self.handProcessor.analyserImage(frame) #On envoie l'image se faire analyser dans le HandTracker
            processedImage = cv2.flip(processedImage,1)
            self.tempsActuel = time.time()
            fps = 1/(self.tempsActuel - self.tempsPrecedent) #Calcul du framerate de la webcam
            self.tempsPrecedent = self.tempsActuel
            processedImage = cv2.putText(processedImage, str(int(fps)), (10,70), cv2.FONT_HERSHEY_DUPLEX,3,(255,0,255),3)
            cv2.imshow(self.nomFenetre, processedImage)
            cv2.setWindowProperty(self.nomFenetre, cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(1)
            if cv2.waitKey(1) == 27:  #Si on appuie sur ESC ça sort de la boucle infinie
                break
        webcamIsOpen = False

    def closeWebcam(self):
        cv2.destroyAllWindows
        self.cam.release