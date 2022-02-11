import cv2
import HandTracker as ht
indexWebcam = 0 #Index de la webcam à utiliser
webcamIsOpen = False
widthWebcam = 640
heightWebcam = 480
nomFenetre = "Webcam"
cam = None

def openWebcam():
    webcamIsOpen = True
    cam = cv2.VideoCapture(indexWebcam) #Ouvre la webcam
    cam.set(3, widthWebcam)
    cam.set(4, heightWebcam)
    while True: #Boucle infinie
        ret,frame = cam.read()
        processedImage = ht.analyserImage(frame)
        cv2.imshow(nomFenetre, cv2.flip(processedImage,1))
        cv2.setWindowProperty(nomFenetre, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
        if cv2.waitKey(1) == 27: #Si on appuie sur ESC ça sort de la boucle infinie
            break
    webcamIsOpen = False

def closeWebcam():
    cv2.destroyAllWindows
    cam.release