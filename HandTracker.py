import cv2
import mediapipe as mp
import numpy
import time

class HandTrackProcessor:
    def __init__(self):
        self.mpMains = mp.solutions.hands
        self.mains = self.mpMains.Hands()
        self.mpDessin = mp.solutions.drawing_utils


    def analyserImage(self, img):
        imgCouleur = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resultats = self.mains.process(imgCouleur)
        if resultats.multi_hand_landmarks != None:
            for reperes in resultats.multi_hand_landmarks:
                self.mpDessin.draw_landmarks(img, reperes, self.mpMains.HAND_CONNECTIONS)
        return img
