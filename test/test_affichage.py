import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import parser
import model

(cadeaux, seconde,reachrange,acccalc) = parser.parseChallenge("a_an_example.in.txt")
heatmap = model.heatMap(reachrange,cadeaux)
heatmap.display()

(cadeaux, seconde,reachrange,acccalc) = parser.parseChallenge("b_better_hurry.in.txt")
heatmap = model.heatMap(reachrange,cadeaux)
heatmap.display()

(cadeaux, seconde,reachrange,acccalc) = parser.parseChallenge("c_carousel.in.txt")
heatmap = model.heatMap(reachrange,cadeaux)
heatmap.display()

(cadeaux, seconde,reachrange,acccalc) = parser.parseChallenge("d_decorated_houses.in.txt")
heatmap = model.heatMap(reachrange,cadeaux)
heatmap.display()

(cadeaux, seconde,reachrange,acccalc) = parser.parseChallenge("e_excellent_weather.in.txt")
heatmap = model.heatMap(reachrange,cadeaux)
heatmap.display()

(cadeaux, seconde,reachrange,acccalc) = parser.parseChallenge("f_festive_flyover.in.txt")
heatmap = model.heatMap(reachrange,cadeaux)
heatmap.display()