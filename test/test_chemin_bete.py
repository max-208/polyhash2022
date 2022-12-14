import os
import sys
import inspect
from scipy.spatial import distance
import math

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from model import cadeau,groupe, heatMap, chemin, boucle, parcoursFinal,traineau
import parser

(cadeaux, secondes, reachRange, Accelerationcalculator) = parser.parseChallenge("d_decorated_houses.in.txt")

heatmap = heatMap(reachRange,cadeaux)
parcoursFinal = parcoursFinal()
while secondes > 0:

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

		value.append(newRow)
	# pour cette région on prend le meilleur point

	maxVal = -math.inf
	maxGroup = None
	groups = maxRegion.getGroups()
	for row in groups:
		for group in row:
			val = group.getScore()*2 - group.getPoids()
			if(val > maxVal):
				maxVal = val
				maxGroup = group

	cheminAller = chemin(groupe(0,0),maxGroup,traineau(reachRange,Accelerationcalculator))
	cheminAller.move()
	cheminRetour = chemin(maxGroup,groupe(0,0),traineau(reachRange,Accelerationcalculator))
	cheminRetour.move()

	bcl = boucle()
	bcl.chemins = [cheminAller,cheminRetour]
	bcl.loadingActions = [["LoadCarrots",bcl.getCarotteConsommes()]]
	for cadeau in maxGroup.cadeaux:
		if(not cadeau.delivre):
			bcl.loadingActions.append(["LoadGift",cadeau.nom])
			cadeau.delivre = True

	print("---")
	print(str(bcl))
	if(secondes - bcl.getTempsConsomme() >= 0):
		parcoursFinal.boucles.append(bcl)
		

print("----------------")
print(str(parcoursFinal))