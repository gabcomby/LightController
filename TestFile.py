import cv2
cam = cv2.VideoCapture(0) #Ouvre la webcam
#Boucle infinie
while True:
    ret,frame = cam.read() #Lis une frame de la caméra
    smaller_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    cv2.imshow('Webcam', frame) #Montre l'image dans une fenêtre
    #Si on appuie sur ESC ça quitte le programme
    if cv2.waitKey(1) == 27:
        break
cam.release() #Ferme la caméra
cv2.destroyAllWindows