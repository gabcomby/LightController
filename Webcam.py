import cv2

def openWebcam():
    cam = cv2.VideoCapture(0) #Ouvre la webcam
    while True: #Boucle infinie
        ret,frame = cam.read() #Lis une frame de la caméra
        smaller_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        cv2.imshow('Webcam', frame) #Montre l'image dans une fenêtre
        if cv2.waitKey(1) == 27: #Si on appuie sur ESC ça quitte le programme
            break
    print("Fermeture de l'application")
    cam.release() #Ferme la caméra
    cv2.destroyAllWindows