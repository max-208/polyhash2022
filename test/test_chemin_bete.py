import os
import sys
import inspect
from scipy.spatial import distance
import math

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from model import cadeau, heatMap
from solver import 
import parser

(cadeaux, secondes, reachRange, Accelerationcalculator) = parser.parseChallenge("d_decorated_houses.in.txt")

heatmap = heatMap(reachRange,cadeaux)

# on détermine la valeur de chaque région
# on prend la région avec la plus grande valeur

value = []
maxVal = -math.inf
maxRegion = None
for row in heatmap.regions:
	newRow = []
	for region in row:
		#TODO : raffiner l'algo de décision
		val = region.getPoids() * -2 + region.getScore()*3 -(distance.euclidean([0,0],[(region.maxX + region.minX) / 2, (region.maxY + region.minY) / 2 ] )//15)** 2
		if(val > maxVal):
			maxVal = val
			maxRegion = region
		newRow.append( [val,region] )
		print("##" if val > 0 else "  ", end="")

	value.append(newRow)
	print("")

print(maxVal)
# pour cette région on prend le meilleur point

print("--------------------------------------------------------------------------")

maxVal = -math.inf
maxGroup = None
groups = maxRegion.getGroups()
for row in groups:
	for group in row:
		val = group.getScore()*2 - group.getPoids()
		if(val > maxVal):
			maxVal = val
			maxGroup = group
		print("#" if val > 0 else " ", end="")
	print("")

