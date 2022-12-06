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
        self.delta_c = a.x - b.x
        self.delta_r = a.y - b.y

    def acc_init(self):
        if self.delta_c >= 1:
            if self.delta_r >= 1:
                self.santa.accelerer(1, "up")
                self.santa.accelerer(1, "right")
            if self.delta_r <= -1:
                self.santa.accelerer(1, "down")
                self.santa.accelerer(1, "right")
            elif self.delta_r == 0:
                self.santa.accelerer(1, "right")
        if self.delta_c <= -1:
            if self.delta_r >= 1:
                self.santa.accelerer(1, "up")
                self.santa.accelerer(1, "left")
            if self.delta_r <= -1:
                self.santa.accelerer(1, "down")
                self.santa.accelerer(1, "left")
            elif self.delta_r == 0:
                self.santa.accelerer(1, "left")


