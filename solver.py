#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import *
from numpy.linalg import norm
import math


class SantaPoint:
    x: int
    y: int

    def __init__(self, a: int = 0, b: int = 0):
        self.x = a
        self.y = b


# creation d'un classe que transport le traineau d'un point a à un point b
# objective: I need to move santa to A and B and change the internal parameters of the traineau
class CheminSimple:
    inicio: SantaPoint
    fin: SantaPoint
    santa: traineau
    delta_c: int
    delta_r: int
    cinematic_vector: list[int, int, bool, int, int, int, int]
    cuadrante: str

    def __init__(self, a: SantaPoint, b: SantaPoint, s: traineau):
        self.inicio = a
        self.fin = b
        self.santa = s
        self.delta_c = b.x - a.x
        self.delta_r = b.y - a.y
        u = [abs(self.delta_c), abs(self.delta_r)] / norm([self.delta_c, self.delta_r])
        a = [math.floor(abs(u[0] * 4)) if abs(u[0] * 4) >= 1 else 1,
             math.floor(abs(u[1] * 4)) if abs(u[1]) * 4 >= 1 else 1]

        #################################### DEFINITION VERCTOR CINEMATIQUE ##########################################
        # vector cinematique :
        # [0] ->acc maximale dans la coordonée c, float type
        # [1] ->acc maximale dans la coordonée r, float type
        # [2] ->il y a un rattrapage? False si il n'y a pas, True si il faut s'arreter deux fois
        # [3] ->acc de rattrapage en c
        # [4] ->acc de rattrapage en r
        # [5] ->Temps d'arrive à la coordonée c
        # [6] ->Temps d'arrive à la coordonée r

        a2 = [0, 0, False, 0, 0, 0, 0]
        if a[0] > abs(self.delta_c):
            a2[0] = self.delta_c
            a2[2] = False
            a2[5] = 1
        elif self.delta_c == 0:
            a2[0] = 0
            a2[2] = False
            a2[5] = 0
        elif self.delta_c % a[0] == 0:
            a2[0] = a[0]
            a2[2] = False
            a2[5] = math.floor(abs(self.delta_c / a[0]))
        else:
            a2[0] = a[0]
            a2[2] = True
            a2[5] = math.floor(abs(self.delta_c / a[0]))
            a2[3] = abs(self.delta_c) % a2[0]

        if a[1] > abs(self.delta_r):
            a2[1] = self.delta_r
            a2[2] = False
            a2[6] = 1
        elif self.delta_r == 0:
            a2[1] = a[1]
            a2[2] = False
            a2[6] = 0
        elif self.delta_r % a[1] == 0:
            a2[1] = a[1]
            a2[2] = False
            a2[6] = math.floor(abs(self.delta_r / a[1]))
        else:
            a2[1] = a[1]
            a2[2] = True
            a2[6] = math.floor(abs(self.delta_r / a[1]))
            a2[4] = abs(self.delta_r) % a2[1]
        self.cinematic_vector = a2
        #################################### DEFINITION CUADRANTE #####################################################
        # On va definit 8 situations differents pour encadrer la navegation de santa
        # l'idee c'est de adapter les action de santa au fur et mesure de la position relative du point de destination

        if 0 < self.cinematic_vector[5] < 5 or 0 < self.cinematic_vector[6] < 5:
            self.cuadrante = 'Movement en L'
        elif self.cinematic_vector[5] == 0 or self.cinematic_vector[6] == 0:
            self.cuadrante = 'Unidirectional Trajectoire'
        elif self.cinematic_vector[5] == self.cinematic_vector[6] and self.cinematic_vector[5] != 0 and self.cinematic_vector[6] != 0:
            self.cuadrante = 'Mouvement diagonal'
        else:
            self.cuadrante = 'Mouvement Mixte'
        ################################################################################################################
    def tracker(self):
        print(self.santa.getPoids(), self.santa.positionX, self.santa.positionY)

    def move(self):
        assert self.santa.nbCarottes >= 6

        self.santa.positionX = self.inicio.x
        self.santa.positionY = self.inicio.y
        self.tracker()
        print("The required mouvement is->")

        if self.cuadrante == 'Mouvement diagonal':
            ################## MOVEMENT DIAGONAL ##########################@
            print("Mouvement diagonal")
            self.acc_diag()
            while self.santa.positionY != self.fin.y and self.santa.positionX != self.fin.x:
                self.tracker()
                self.santa.flotter(1)
            self.stop_r()
            self.tracker()
            self.santa.flotter(1)
            self.stop_c()
            self.tracker()
            print("Fin du chemin")


    def acc_diag(self):
        if self.delta_c >= 1:
            if self.delta_r >= 1:
                self.santa.accelerer(self.cinematic_vector[0], "up")
                self.santa.flotter(1)
                self.santa.accelerer(self.cinematic_vector[0], "right")

            if self.delta_r <= -1:
                self.santa.accelerer(self.cinematic_vector[0], "down")
                self.santa.flotter(1)
                self.santa.accelerer(self.cinematic_vector[0], "right")

            elif self.delta_r == 0:
                self.santa.accelerer(self.cinematic_vector[0], "right")
        if self.delta_c <= -1:
            if self.delta_r >= 1:
                self.santa.accelerer(self.cinematic_vector[1], "up")
                self.santa.flotter(1)
                self.santa.accelerer(self.cinematic_vector[1], "left")

            if self.delta_r <= -1:
                self.santa.accelerer(self.cinematic_vector[1], "down")
                self.santa.flotter(1)
                self.santa.accelerer(self.cinematic_vector[1], "left")

            elif self.delta_r == 0:
                self.santa.accelerer(self.cinematic_vector[1], "left")

        elif self.delta_c == 0 and self.delta_r >= 1:
            self.santa.accelerer(self.cinematic_vector[0], "up")

        elif self.delta_c == 0 and self.delta_r <= -1:
            self.santa.accelerer(self.cinematic_vector[1], "down")

    def stop_c(self):
        self.tracker()
        if not self.cinematic_vector[3]:
            if self.delta_c >= 1:
                self.santa.accelerer(self.cinematic_vector[0], "left")
            if self.delta_c <= -1:
                self.santa.accelerer(self.cinematic_vector[0], "right")

    def stop_r(self):
        self.tracker()
        if not self.cinematic_vector[3]:
            if self.delta_r >= 1:
                self.santa.accelerer(self.cinematic_vector[1], "down")
            if self.delta_r <= -1:
                self.santa.accelerer(self.cinematic_vector[1], "up")



P1 = SantaPoint(40, 40)
P2 = SantaPoint(30,30)
S1 = traineau(3)
S1.chargerCarotte(10)
C1 = CheminSimple(P1, P2, S1)
print(C1.cinematic_vector)
C1.move()
