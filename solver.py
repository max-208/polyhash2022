#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from model import groupe,chemin,accelerationCalculator
from numpy.linalg import norm
import math

P1 = groupe(0, 0)
P2 = groupe(-284, 142)
C1 = chemin(P1, P2, 3, accelerationCalculator([[math.inf,4]]))
C1.move()
