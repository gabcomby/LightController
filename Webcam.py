import cv2

class Webcam :
    def __init__(self):
        self.indexWebcam = 0
        self.webcamIsOpen = False
        self.widthWebcam = 640
        self.heightWebcam = 480
        self.nomFenetre = "Webcam"
        self.cam = None

    #Attribue la webcam à notre programme et démarre la boucle infinie de lecture de la caméra
    def openWebcam(self): #Ouvre la webcam et set ses dimentions
        self.webcamIsOpen = True
        self.cam = cv2.VideoCapture(self.indexWebcam)
        self.cam.set(3, self.widthWebcam)
        self.cam.set(4, self.heightWebcam)

    #Lis une image de la webcam et la retourne
    def readWebcam(self):
        ret, frame = self.cam.read()
        cv2.waitKey(1)
        return frame

    #Ferme la webcam de manière sécuritaire
    def closeWebcam(self):
        cv2.destroyAllWindows
        self.cam.release