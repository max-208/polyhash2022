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

    def __init__(self, a: SantaPoint, b: SantaPoint, s: traineau):
        self.inicio = a
        self.fin = b
        self.santa = s
        self.delta_c = b.x - a.x
        self.delta_r = b.y - a.y

    def acc_max(self) -> list[int, int, bool, int, int, int, int]:
        u = [abs(self.delta_c), abs(self.delta_r)] / norm([self.delta_c, self.delta_r])
        a = [math.floor(abs(u[0] * 4)), math.floor(abs(u[1] * 4))]
        a2 = [0, 0, False, 0, 0, 0, 0]
        if a[0] > abs(self.delta_c):
            a2[0] = self.delta_c
            a2[2] = False
            a2[5] = 1
        elif a[0] % self.delta_c == 0:
            a2[0] = a[0]
            a2[2] = False
            a2[5] = math.floor(abs(self.delta_c / a2[0]))
        else:
            a2[0] = a[0]
            a2[2] = True
            a2[5] = math.floor(abs(self.delta_c / a2[0]))

        if a[1] > abs(self.delta_r):
            a2[1] = self.delta_r
            a2[2] = False
            a2[6] = 1
        elif a[1] % self.delta_r == 0:
            a2[1] = a[1]
            a2[2] = False
            a2[6] = math.floor(abs(self.delta_r / a2[1]))
        else:
            a2[1] = a[1]
            a2[2] = True
            a2[6] = math.floor(abs(self.delta_r / a2[1]))

        a2[3] = abs(self.delta_c) % a2[0]
        a2[4] = abs(self.delta_r) % a2[1]

        print("the max acceleration possible is : ", a, a2)
        return a2

    def acc_init(self):
        cinematic_vector = self.acc_max()
        if self.delta_c >= 1:
            if self.delta_r >= 1:
                self.santa.accelerer(cinematic_vector[0], "up")
                self.santa.flotter(1)
                self.santa.accelerer(cinematic_vector[0], "right")

            if self.delta_r <= -1:
                self.santa.accelerer(cinematic_vector[0], "down")
                self.santa.flotter(1)
                self.santa.accelerer(cinematic_vector[0], "right")

            elif self.delta_r == 0:
                self.santa.accelerer(cinematic_vector[0], "right")

        if self.delta_c <= -1:
            if self.delta_r >= 1:
                self.santa.accelerer(cinematic_vector[1], "up")
                self.santa.flotter(1)
                self.santa.accelerer(cinematic_vector[1], "left")

            if self.delta_r <= -1:
                self.santa.accelerer(cinematic_vector[1], "down")
                self.santa.flotter(1)
                self.santa.accelerer(cinematic_vector[1], "left")

            elif self.delta_r == 0:
                self.santa.accelerer(cinematic_vector[1], "left")

        elif self.delta_c == 0 and self.delta_r >= 1:
            self.santa.accelerer(cinematic_vector[0], "up")

        elif self.delta_c == 0 and self.delta_r <= -1:
            self.santa.accelerer(cinematic_vector[1], "down")

    def stop_c(self):
        cinematic_vector = self.acc_max()
        if self.delta_c >= 1:
            self.santa.accelerer(cinematic_vector[0], "left")
        if self.delta_c <= -1:
            self.santa.accelerer(cinematic_vector[0], "right")

    def stop_r(self):
        cinematic_vector = self.acc_max()
        if self.delta_r >= 1:
            self.santa.accelerer(cinematic_vector[1], "down")
        if self.delta_r <= -1:
            self.santa.accelerer(cinematic_vector[1], "up")

    def tracker(self):
        print(self.santa.getPoids(), self.santa.positionX, self.santa.positionY)

    def move(self):
        assert self.santa.nbCarottes >= 6
        cinematic_vector = self.acc_max()
        self.santa.positionX = self.inicio.x
        self.santa.positionY = self.inicio.y
        self.tracker()
        self.acc_init()
        self.tracker()

        while self.santa.positionY != self.fin.y - cinematic_vector[0] - cinematic_vector[3]:
            self.tracker()
            self.santa.flotter(1)
        self.santa.flotter(1)
        print("on va stop")
        self.stop_r()
        self.tracker()
        self.santa.flotter(1)
        self.stop_c()
        self.tracker()


P1 = SantaPoint(0, 0)
P2 = SantaPoint(60, 60)
S1 = traineau(3)
S1.chargerCarotte(10)
C1 = CheminSimple(P1, P2, S1)
C1.move()
