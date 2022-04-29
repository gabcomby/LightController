import cv2
import mediapipe as mp
import os
import tensorflow as tf
from tensorflow.python import keras
from keras.models import load_model
import numpy as np

#Désactive CUDA sur tous les appareils pour éviter des problèmes de compatibilité Windows/Mac et Desktop/Laptop
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

#Charge le modèle de reconnaissance de gestes dans TensorFlow & Keras
handGestureModel = load_model('./hand_gesture_dataset')
'''
Le modèle TensorFlow utilisé provient de ce tutoriel détaillé que nous avons trouvé en ligne:
https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/
Nous avons aussi utilisé ce tutoriel comme complément à celui sur Mediapipe afin de nous assurer que la reconnaissance
de nos mains était correctement implémentée.
'''

#Charge les noms des différentes gestes
fichier = open('./hand_gesture.names', 'r')
handGestureNames = fichier.read().split('\n')
fichier.close()

class HandTrackProcessor:
    def __init__(self, seuilDetection = 0.7, seuilTracking = 0.5):
        self.detectionMin = seuilDetection
        self.trackMin = seuilTracking
        self.mpMains = mp.solutions.hands
        self.mains = self.mpMains.Hands(False, 1, 1, self.detectionMin, self.trackMin)
        self.mpDessin = mp.solutions.drawing_utils
        self.listeMarqueurs = [None]*21
        self.pastNomGeste = None

    def analyserImage(self, img):
        indexMarqueur = 0
        h, w, c = img.shape
        imgCouleur = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #Analyse l'image à la recherche d'une main
        self.resultats = self.mains.process(imgCouleur)
        #Si le programme trouve une main, entre dans cette boucle
        if self.resultats.multi_hand_landmarks != None:
            for reperes in self.resultats.multi_hand_landmarks: #Passe à travers les données de tous les points de repère de la main
                self.mpDessin.draw_landmarks(img, reperes, self.mpMains.HAND_CONNECTIONS) #Dessine les points de repère et les lignes qui les relie sur la main
                for lm in reperes.landmark: #Pour chaque repère, on analyse le ID et les positions X&Y
                    cx, cy = int(lm.x*w), int(lm.y*h) #Calcule la position en X&Y relative à la taille de la caméra des repères de la main (en pixels)
                    self.listeMarqueurs[indexMarqueur] = (cx, cy) #Ajoute les positions X&Y selon le ID du marqueur dans un tableau
                    indexMarqueur = indexMarqueur+1
        return img, self.listeMarqueurs

    #Méthode qui analyse les points de la main et détecte le mouvement de celle-ci
    def predictionGeste(self, listeMarqueurs):
        prediction = handGestureModel.predict([listeMarqueurs])
        IDGeste = np.argmax(prediction)
        nomGeste = handGestureNames[IDGeste]
        #Retourne le nom du geste si ce dernier est différent de celui détecté précédemment
        if nomGeste != None :
            if(nomGeste != self.pastNomGeste):
                self.pastNomGeste = nomGeste
                return nomGeste