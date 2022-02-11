import Webcam as wc

print("╔═══════════════════════╗")
print(" HandController V. 0.1.0")
print("╚═══════════════════════╝")
webcam = wc.Webcam()
webcam.openWebcam()
while webcam.webcamIsOpen == True:
    continue
if webcam.webcamIsOpen == False:
    webcam.closeWebcam
print("Fermeture de l'application")