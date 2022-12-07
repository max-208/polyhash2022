#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import *

class SantaPoint:
    x: int
    y: int

    def __init__(self, a: int = 0, b: int = 0):
        self.x = a
        self.y = b


# creation d'un classe que transport le traineua d'un point a à un point b
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

    def acc_init(self):
        if self.delta_c >= 1:
            if self.delta_r >= 1:
                self.santa.accelerer(1, "up")
                self.santa.flotter(1)
                self.santa.accelerer(1, "right")
                self.santa.flotter(1)
            if self.delta_r <= -1:
                self.santa.accelerer(1, "down")
                self.santa.flotter(1)
                self.santa.accelerer(1, "right")
                self.santa.flotter(1)
            elif self.delta_r == 0:
                self.santa.accelerer(1, "right")
                self.santa.flotter(1)
        if self.delta_c <= -1:
            if self.delta_r >= 1:
                self.santa.accelerer(1, "up")
                self.santa.flotter(1)
                self.santa.accelerer(1, "left")
                self.santa.flotter(1)
            if self.delta_r <= -1:
                self.santa.accelerer(1, "down")
                self.santa.flotter(1)
                self.santa.accelerer(1, "left")
                self.santa.flotter(1)
            elif self.delta_r == 0:
                self.santa.accelerer(1, "left")
                self.santa.flotter(1)
        elif self.delta_c == 0 and self.delta_r >= 1:
            self.santa.accelerer(1, "up")
            self.santa.flotter(1)
        elif self.delta_c == 0 and self.delta_r <= -1:
            self.santa.accelerer(1, "down")
            self.santa.flotter(1)

    def stop_c(self):
        if self.delta_c >= 1:
            self.santa.accelerer(1, "left")
        if self.delta_c <= -1:
            self.santa.accelerer(1, "right")

    def stop_r(self):
        if self.delta_r >= 1:
            self.santa.accelerer(1, "down")
        if self.delta_r <= -1:
            self.santa.accelerer(1, "up")
    def tracker(self): #Afficher infor du traineau
        print(self.santa.getPoids(),self.santa.positionX,self.santa.positionY)

    def move(self):
        self.acc_init()
        self.tracker()
        t = 0
        if self.santa.positionY != a.y-1 and self.santa.positionX =! a.x-1:
            self.tracker()
            self.santa.flotter(t)
            t += 1
        else:
            self.santa.flotter(1)
            self.stop_r()
            self.santa.flotter(1)
            self.stop_c()




P1 = SantaPoint(0, 0)
P2 = SantaPoint(5, 5)
S1 = traineau(3)
S1.chargerCarotte(10)
C1= CheminSimple(P1, P2, S1)
C1.acc_init()
C1.tracker()
S1.flotter(1)
C1.tracker()

