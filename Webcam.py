import cv2
import HandTracker as ht
class Webcam :
    def __init__(self):
        self.closeWebcam = None
        self.indexWebcam = 0
        self.webcamIsOpen = False
        self.widthWebcam = 640
        self.heightWebcam = 480
        self.nomFenetre = "Webcam"
        self.cam = None

    def openWebcam(self):
        webcamIsOpen = True
        cam = cv2.VideoCapture(self.indexWebcam)  # Ouvre la webcam
        cam.set(3, self.widthWebcam)
        cam.set(4, self.heightWebcam)
        while True:  # Boucle infinie
            ret, frame = cam.read()
            processedImage = ht.analyserImage(frame)
            cv2.imshow(self.nomFenetre, cv2.flip(processedImage, 1))
            cv2.setWindowProperty(self.nomFenetre, cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(1)
            if cv2.waitKey(1) == 27:  # Si on appuie sur ESC ça sort de la boucle infinie
                break
        webcamIsOpen = False

    def closeWebcam(self):
        cv2.destroyAllWindows
        self.cam.release