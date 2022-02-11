import Webcam as wc

print("╔═══════════════════════╗")
print(" HandController V. 1.0.0")
print("╚═══════════════════════╝")
"""""
reponse = input("Consentez-vous à l'utilisation de votre webcam (O/N) : ")
reponse = reponse.lower()
if reponse == "oui" or reponse == "o":
    wc.openWebcam()
else:
    print("Fermeture de l'application")
"""""
webcam = wc.Webcam()
webcam.openWebcam()
while webcam.webcamIsOpen == True:
    continue
if webcam.webcamIsOpen == False:
    webcam.closeWebcam
print("Fermeture de l'application")