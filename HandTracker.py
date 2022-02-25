import cv2
import mediapipe as mp
import tensorflow as tf
from tensorflow.python import keras
from keras.models import load_model
import numpy as np

#Charge le modèle de reconnaissance de gestes dans TensorFlow & Keras
handGestureModel = load_model('hand_gesture_dataset')

#Charge les noms des différentes gestes
fichier = open('hand_gesture.names', 'r')
handGestureNames = fichier.read().split('\n')
fichier.close()

class HandTrackProcessor:
    def __init__(self, detectionTreshold = 0.7, trackTreshold = 0.5):
        self.detectionMin = detectionTreshold
        self.trackMin = trackTreshold
        self.mpMains = mp.solutions.hands
        self.mains = self.mpMains.Hands(False, 1, 1, self.detectionMin, self.trackMin)
        self.mpDessin = mp.solutions.drawing_utils
        self.listeMarqueurs = [None]*21


    def analyserImage(self, img):
        indexMarqueur = 0
        h, w, c = img.shape
        imgCouleur = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.resultats = self.mains.process(imgCouleur) #Analyse l'image à la recherche d'une main
        if self.resultats.multi_hand_landmarks != None:
            for reperes in self.resultats.multi_hand_landmarks: #Passe à travers les données de tous les points de repère de la main
                self.mpDessin.draw_landmarks(img, reperes, self.mpMains.HAND_CONNECTIONS) #Dessine les points de repère et les lignes qui les relie sur la main
                for lm in reperes.landmark: #Pour chaque repère, on analyse le ID et les positions X&Y
                    cx, cy = int(lm.x*w), int(lm.y*h) #Calcule la position en X&Y relative à la taille de la caméra des repères de la main (en pixels)
                    self.listeMarqueurs[indexMarqueur] = (cx, cy) #Ajoute les positions X&Y selon le ID du marqueur dans un tableau
                    indexMarqueur = indexMarqueur+1
        return img, self.listeMarqueurs

    def predictionGeste(self, listeMarqueurs):
        prediction = handGestureModel.predict([listeMarqueurs])
        IDGeste = np.argmax(prediction)
        nomGeste = handGestureNames[IDGeste]
        print(nomGeste)