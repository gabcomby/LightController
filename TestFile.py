import cv2 #Importe la librairie OpenCV
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print('Oh no!')
while True:
    ret,frame = cam.read() #ret est un boolean, frame est une image
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break
cam.release() #Ferme la caméra
cv2.destroyAllWindows