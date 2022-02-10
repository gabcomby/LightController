import Webcam
print("╔═══════════════════════╗")
print(" HandController V. 1.0.0")
print("╚═══════════════════════╝")
reponse = input("Consentez-vous à l'utilisation de votre webcam (O/N) : ")
reponse = reponse.lower()
if reponse == "oui" or reponse == "o":
    Webcam.openWebcam()
else:
    print("Fermeture de l'application")
while Webcam.webcamIsOpen == True:
    continue
print("Fermeture de l'application")