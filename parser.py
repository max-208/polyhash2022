#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import traineau, accelerationCalculator, cadeau
import os

def parseChallenge(filename):
    #filename = "a_an_example.in.txt"
    filename = os.path.dirname(__file__) + "/" + filename
    with open(filename, 'r') as a_fichier:
        contenu = a_fichier.readlines()

    weightsParAccel = list()
    cadeaux = list()
    traineaux = list()

    for ligne in contenu:
        if contenu.index(ligne) == 0:
            secondes = int(ligne.split()[0])
            reachRangeTraineau = int(ligne.split()[1])
            accel_range = int(ligne.split()[2])
            nb_cadeaux = int(ligne.split()[3])

        elif 1 <= contenu.index(ligne) <= accel_range:
            weightsParAccel.append([int(ligne.split()[0]), int(ligne.split()[1])])

        elif accel_range < contenu.index(ligne) <= (accel_range + nb_cadeaux):
            cadeaux.append(cadeau(ligne.split()[0], int(ligne.split()[2]), int(ligne.split()[1]), int(ligne.split()[3]),int(ligne.split()[4])))

    Accelerationcalculator = accelerationCalculator(weightsParAccel)

    return cadeaux, secondes, reachRangeTraineau, Accelerationcalculator
