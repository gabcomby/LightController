import cv2
import mediapipe as mp
import os
import tensorflow as tf
from tensorflow.python import keras
from keras.models import load_model
import numpy as np

#Désactive CUDA sur tous les appareils pour éviter des problèmes de compatibilité Windows/Mac et Desktop/Laptop
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

#Charge le modèle de reconnaissance de gestes dans TensorFlow
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

'''
Objet qui va permettre de détecter la main, de la suivre, d'analyser la position de 21 points distincts sur celle-ci
et de feed ces données au modèle TensorFlow
'''
class HandTrackProcessor:
    def __init__(self, seuilDetection = 0.7, seuilTracking = 0.5):
        #Change la sensibilité de la détection des mains de Mediapipe
        self.detectionMin = seuilDetection
        #Change la sensibilité du suivi des mains de Mediapipe
        self.trackMin = seuilTracking
        self.mpMains = mp.solutions.hands
        #Crée l'outil de suivi des mains avec les paramètres de sensibilité ce-dessus et une limite de 1 main à la fois
        self.mains = self.mpMains.Hands(False, 1, 1, self.detectionMin, self.trackMin)
        #Crée l'outil qui va dessiner les traits sur la main qui est suivie
        self.mpDessin = mp.solutions.drawing_utils
        #Crée une liste vide dans laquelle nous stockerons les coordonnées des 21 points
        self.listeMarqueurs = [None]*21
        self.pastNomGeste = None

    '''
    Méthode utilisant Mediapipe pour suivre la main et trouver les coordonnées de 21 points sur celle-ci
    '''
    def analyserImage(self, img):
        #Index du point à analyser
        indexMarqueur = 0
        #Prends la hauteur et la largeur de l'image que l'on passe à Mediapipe
        h, w, c = img.shape
        #Convertis l'image dans un format de couleur BGR2RGB (le format utilisé par Mediapipe)
        imgCouleur = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #Analyse l'image à la recherche d'une main
        self.resultats = self.mains.process(imgCouleur)
        #Si le programme trouve une main, entre dans cette boucle
        if self.resultats.multi_hand_landmarks != None:
            for reperes in self.resultats.multi_hand_landmarks: #Passe à travers les données de tous les points de repère de la main
                self.mpDessin.draw_landmarks(img, reperes, self.mpMains.HAND_CONNECTIONS) #Dessine les points de repère et les lignes qui les relient sur la main
                for lm in reperes.landmark: #Pour chaque repère, on analyse le ID et les positions X&Y dans l'espace
                    cx, cy = int(lm.x*w), int(lm.y*h) #Calcule la position en X&Y relative à la taille de l'image des repères de la main (en pixels)
                    self.listeMarqueurs[indexMarqueur] = (cx, cy) #Ajoute les positions X&Y selon le ID du marqueur dans un tableau
                    indexMarqueur = indexMarqueur+1 #Ajoute 1 à l'index, de manière à ce qu'on analyse les 21 points un par un
        return img, self.listeMarqueurs #Retourne l'image avec les points&lignes ainsi que le tableau des coordonnées des points dans le Main

    '''
    Méthode faisant appel à un modèle TensorFlow auquel on passe les coordonnées des 21 points trouvées grâce à la
    méthode analyserImage(), et qui analyse ces points afin de déterminer quel geste de la main nous faisons
    '''
    def predictionGeste(self, listeMarqueurs):
        #Envoie les 21 points au modèle afin de prédire quel geste est fait devant la caméra
        prediction = handGestureModel.predict([listeMarqueurs])
        #Choisis l'ID du geste ayant la plus haute probabilité d'être celui effectué devant la caméra
        IDGeste = np.argmax(prediction)
        #Sélectionne le nom du geste associé à l'ID choisis
        nomGeste = handGestureNames[IDGeste]
        #Retourne le nom du geste si ce dernier est différent de celui détecté précédemment (afin d'éviter le spam du
        #même geste en boucle)
        if nomGeste != None :
            if(nomGeste != self.pastNomGeste):
                self.pastNomGeste = nomGeste
                return nomGeste