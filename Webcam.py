import cv2

'''
Crée un objet qui permet de contrôler la webcam
'''
class Webcam :
    def __init__(self):
        #Index de la webcam de l'ordinateur
        self.indexWebcam = 0
        self.webcamIsOpen = False
        #Résolution de l'image que l'on veut capturer
        self.widthWebcam = 640
        self.heightWebcam = 480
        self.nomFenetre = "Webcam"
        self.cam = None

    #Attribue la webcam à notre programme et démarre la boucle infinie de lecture de la caméra
    def openWebcam(self):
        self.webcamIsOpen = True
        #Crée la webcam (attribue l'appareil physique au programme)
        self.cam = cv2.VideoCapture(self.indexWebcam)
        #Set la résolution de l'image à celle spécifiée plus haut
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