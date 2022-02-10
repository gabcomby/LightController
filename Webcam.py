import cv2
indexWebcam = 0 #Index de la webcam à utiliser
webcamIsOpen = False
widthWebcam = 640
heightWebcam = 480

def openWebcam():
    webcamIsOpen = True
    cam = cv2.VideoCapture(indexWebcam) #Ouvre la webcam
    cam.set(3, widthWebcam)
    cam.set(4, heightWebcam)
    while True: #Boucle infinie
        ret,frame = cam.read()
        cv2.imshow('Webcam', frame)
        cv2.waitKey(1)
        if cv2.waitKey(1) == 27: #Si on appuie sur ESC ça sort de la boucle infinie
            break
    webcamIsOpen = False

def closeWebcam():
    cv2.destroyAllWindows
    openWebcam.cam.release