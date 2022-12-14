#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import *
from numpy.linalg import norm
import math

P1 = groupe(0, 10)
P2 = groupe(0, 0)
S1 = traineau(3, accelerationCalculator([[100,4],[150,0]]))
S1.chargerCarotte(40)
C1 = chemin(P1, P2, S1)
print(C1.cinematic_vector)
print(C1.quadrant)
C1.move()
