import cv2
import mediapipe as mp

class HandTrackProcessor:
    def __init__(self, detectionTreshold = 0.7, trackTreshold = 0.5):
        self.detectionMin = detectionTreshold
        self.trackMin = trackTreshold
        self.mpMains = mp.solutions.hands
        self.mains = self.mpMains.Hands(False, 2, 1, self.detectionMin, self.trackMin)
        self.mpDessin = mp.solutions.drawing_utils


    def analyserImage(self, img):
        imgCouleur = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.resultats = self.mains.process(imgCouleur) #Analyse l'image à la recherche d'une main
        if self.resultats.multi_hand_landmarks != None:
            for reperes in self.resultats.multi_hand_landmarks: #Passe à travers les données de tous les points de repère de la main
                self.mpDessin.draw_landmarks(img, reperes, self.mpMains.HAND_CONNECTIONS) #Dessine les points de repère et les lignes qui les relie sur la main
        return img


    def positionMain(self, img):
        listeMarqueurs = []
        if self.resultats.multi_hand_landmarks != None:
            for reperes in self.resultats.multi_hand_landmarks:
                for id, lm in enumerate(reperes.landmark): #Pour chaque repère, on analyse le ID et les positions X&Y
                    h, w, c = img.shape #Get la hauteur et la largeur de l'image de la webcam
                    cx, cy = int(lm.x*w), int(lm.y*h) #Calcule la position en X&Y relative à la taille de la caméra des repères de la main (en pixels)
                    listeMarqueurs.append([id, cx, cy]) #Ajoute les positions X&Y selon le ID du marqueur dans un tableau
        return listeMarqueurs