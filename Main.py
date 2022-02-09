import Webcam
print("Test de l'utilisation de la Webcam")
reponse = input("Consentez-vous à l'utilisation de votre webcam (O/N) : ")
reponse = reponse.lower()
if reponse == "oui" or reponse == "o":
    Webcam.openWebcam()
else:
    print("Fermeture de l'application")