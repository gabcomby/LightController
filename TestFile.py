import cv2 #Importe la librairie OpenCV
imgInitiale = cv2.imread('Image/imageTest.png', 1) #Lis le fichier PNG de l'image dans le dossier 'Image'
imgFinale = cv2.resize(imgInitiale, (600,600)) #Resize l'image à une dimension de 600x600 au lieu de 400x400
imgInitiale = cv2.rotate(imgFinale, cv2.ROTATE_90_CLOCKWISE) #Rotate l'image de 90 degrés dans le sens des aiguilles d'une montre
cv2.imshow('Image de test', imgInitiale) #Affiche l'image dans une fenêtre ayant pour titre 'Image de test'
cv2.waitKey(0) #Attends indéfiniment que l'utilisateur clique sur une touche quelconque du clavier
cv2.destroyAllWindows #Ferme la fenêtre