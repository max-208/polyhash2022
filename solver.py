#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import *
from numpy.linalg import norm
import math

P1 = groupe(54, 302)
P2 = groupe(0, 0)
C1 = chemin(P1, P2, 3, accelerationCalculator([[math.inf,4]]))
print(C1.cinematic_vector)
print(C1.quadrant)
C1.move()
