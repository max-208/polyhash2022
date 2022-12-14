#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import *
from numpy.linalg import norm
import math

P1 = groupe(0, 0)
P2 = groupe(5, 1)
S1 = traineau(3, accelerationCalculator([[60,2]]))
S1.chargerCarotte(40)
C1 = chemin(P1, P2, S1)
print(C1.cinematic_vector)
print(C1.quadrant)
C1.move()
