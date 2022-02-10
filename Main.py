import Webcam as wc
import cv2

print("╔═══════════════════════╗")
print(" HandController V. 1.0.0")
print("╚═══════════════════════╝")
reponse = input("Consentez-vous à l'utilisation de votre webcam (O/N) : ")
reponse = reponse.lower()
if reponse == "oui" or reponse == "o":
    wc.openWebcam()
else:
    print("Fermeture de l'application")

while wc.webcamIsOpen == True:
    continue
if wc.webcamIsOpen == False:
    wc.closeWebcam
print("Fermeture de l'application")