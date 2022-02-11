import cv2
import mediapipe as mp
import numpy
import time

mpMains = mp.solutions.hands
mains = mpMains.Hands()
mpDessin = mp.solutions.drawing_utils

def analyserImage(img):
    imgCouleur = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultats = mains.process(imgCouleur)
    if resultats.multi_hand_landmarks != None:
        for reperes in resultats.multi_hand_landmarks:
            mpDessin.draw_landmarks(img, reperes, mpMains.HAND_CONNECTIONS)
    return img
