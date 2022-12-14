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
    cinematic_vector: list[int, int, bool, int, int, int, int, bool]
    cuadrante: str

    def __init__(self, a: SantaPoint, b: SantaPoint, s: traineau):
        self.inicio = a
        self.fin = b
        self.santa = s
        self.delta_c = b.x - a.x
        self.delta_r = b.y - a.y
        u = [abs(self.delta_c), abs(self.delta_r)] / norm([self.delta_c, self.delta_r])
        a = [math.floor(abs(u[0] * self.santa.accelerationUpperBound)) if abs(
            u[0] * self.santa.accelerationUpperBound) >= 1 else 1,
             math.floor(abs(u[1] * self.santa.accelerationUpperBound)) if abs(
                 u[1] * self.santa.accelerationUpperBound) >= 1 else 1]

        #################################### DEFINITION VERCTOR CINEMATIQUE ##########################################
        # vector cinematique :
        # [0] ->acc maximale dans la coordonée c, float type
        # [1] ->acc maximale dans la coordonée r, float type
        # [2] ->il y a un rattrapage en c? False si il n'y a pas, True si il faut s'arreter deux fois
        # [3] ->acc de rattrapage en c
        # [4] ->acc de rattrapage en r
        # [5] ->Temps d'arrive à la coordonée c
        # [6] ->Temps d'arrive à la coordonée r
        # [7] ->il y a un rattrapage en r? False si il n'y a pas, True si il faut s'arreter deux fois

        a2 = [0, 0, False, 0, 0, 0, 0, False]
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
            a2[7] = False
            a2[6] = 1
        elif self.delta_r == 0:
            a2[1] = a[1]
            a2[7] = False
            a2[6] = 0
        elif self.delta_r % a[1] == 0:
            a2[1] = a[1]
            a2[7] = False
            a2[6] = math.floor(abs(self.delta_r / a[1]))
        else:
            a2[1] = a[1]
            a2[7] = True
            a2[6] = math.floor(abs(self.delta_r / a[1]))
            a2[4] = abs(self.delta_r) % a2[1]
        self.cinematic_vector = a2
        #################################### DEFINITION CUADRANTE #####################################################
        # On va definit 8 situations differents pour encadrer la navegation de santa
        # l'idee c'est de adapter les action de santa au fur et mesure de la position relative du point de destination
        if self.cinematic_vector[5] == self.cinematic_vector[6] and self.cinematic_vector[5] != 0 and \
                self.cinematic_vector[6] != 0:
            self.cuadrante = 'Mouvement diagonal'
        else:
            self.cuadrante = 'Mouvement en L'
        # elif self.cinematic_vector[5] == 0 or self.cinematic_vector[6] == 0:
        #     self.cuadrante = 'Trajectoire Unidirectional'
        #
        # else:
        #     self.cuadrante = 'Mouvement Mixte'
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
            if self.cinematic_vector[2]:
                self.set_c()
                self.tracker()
            if self.cinematic_vector[7]:
                self.set_r()
            self.tracker()
            self.acc_c()
            self.santa.flotter(1)
            self.acc_r()
            self.santa.flotter(self.cinematic_vector[5] - 1)
            self.stop_c()
            self.santa.flotter(1)
            self.stop_r()
            self.tracker()
            print("fin du mouvement")
        if self.cuadrante == 'Mouvement en L':
            print("Mouvement L")
            # identifier le chemin court
            Direction = self.cinematic_vector.index(min(self.cinematic_vector[5], self.cinematic_vector[6]), 2)

            if Direction == 5:  # le mouvement demarre en c
                if self.cinematic_vector[2]:
                    self.set_c()
                self.tracker()
                self.acc_c()
                self.santa.flotter(self.cinematic_vector[5])
                self.stop_c()
                # Après on continue sur l'axis r
                self.santa.flotter(1)
                if self.cinematic_vector[7]:
                    self.set_r()
                self.tracker()
                self.acc_r()
                self.santa.flotter(self.cinematic_vector[6])
                self.tracker()
                self.stop_r()
                self.tracker()
                print("fin du chemin")
            elif Direction == 6:  # le mouvement demarre en r
                if self.cinematic_vector[7]:
                    self.set_r()
                self.tracker()
                self.acc_r()
                self.santa.flotter(self.cinematic_vector[6])
                self.stop_r()
                # on continue sur l'axis c
                self.santa.flotter(1)
                if self.cinematic_vector[2]:
                    self.set_c()
                self.tracker()
                self.acc_c()
                self.santa.flotter(self.cinematic_vector[5])
                self.tracker()
                self.stop_c()
                self.tracker()
                print("fin du chemiiiin")

    def set_c(self):  # function qui va régler le rattrapage dans la coordonée c
        if self.delta_c >= 1:
            self.santa.accelerer(self.cinematic_vector[3], "right")
            self.santa.flotter(1)
            self.santa.accelerer(self.cinematic_vector[3], "left")
            self.santa.flotter(1)

        elif self.delta_c <= -1:
            self.santa.accelerer(self.cinematic_vector[3], "left")
            self.santa.flotter(1)
            self.santa.accelerer(self.cinematic_vector[3], "right")
            self.santa.flotter(1)

    def set_r(self):  # function qui va régler le rattrapage dans la coordonée r
        if self.delta_r >= 1:
            self.santa.accelerer(self.cinematic_vector[4], "up")
            self.santa.flotter(1)
            self.santa.accelerer(self.cinematic_vector[4], "down")
            self.santa.flotter(1)
        elif self.delta_r <= -1:
            self.santa.accelerer(self.cinematic_vector[4], "down")
            self.santa.flotter(1)
            self.santa.accelerer(self.cinematic_vector[4], "up")
            self.santa.flotter(1)

    def acc_c(self):
        assert self.delta_c != 0
        assert self.santa.nbCarottes > 6
        if self.delta_c > 1:
            self.santa.accelerer(self.cinematic_vector[0], "right")
        else:
            self.santa.accelerer(self.cinematic_vector[0], "left")

    def acc_r(self):
        assert self.delta_r != 0
        assert self.santa.nbCarottes > 6
        if self.delta_r > 1:
            self.santa.accelerer(self.cinematic_vector[1], "up")
        else:
            self.santa.accelerer(self.cinematic_vector[1], "down")

    def stop_c(self):
        self.tracker()
        if self.delta_c >= 1:
            self.santa.accelerer(self.cinematic_vector[0], "left")
        if self.delta_c <= -1:
            self.santa.accelerer(self.cinematic_vector[0], "right")

    def stop_r(self):
        self.tracker()
        if self.delta_r >= 1:
            self.santa.accelerer(self.cinematic_vector[1], "down")
        if self.delta_r <= -1:
            self.santa.accelerer(self.cinematic_vector[1], "up")


P1 = SantaPoint(0, 0)
P2 = SantaPoint(10, 3)
S1 = traineau(3)
S1.chargerCarotte(20)
C1 = CheminSimple(P1, P2, S1)
print(C1.cinematic_vector)
print(C1.cuadrante)
C1.move()
