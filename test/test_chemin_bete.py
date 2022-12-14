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

(cadeaux, secondes, reachRange, Accelerationcalculator) = parser.parseChallenge("b_better_hurry.in.txt")

heatmap = heatMap(reachRange,cadeaux)
parcoursFinal = parcoursFinal()
maxVal = 0
while (secondes > 0 and maxVal != -math.inf):

	# on détermine la valeur de chaque région
	# on prend la région avec la plus grande valeur
	maxVal = -math.inf
	maxRegion = None
	for row in heatmap.regions:
		for region in row:
			#TODO : raffiner l'algo de décision
			if(region.getScore() == 0):
				val = -math.inf
			else:
				val = region.getPoids() * -2 + region.getScore()*3 -(distance.euclidean([0,0],[(region.maxX + region.minX) / 2, (region.maxY + region.minY) / 2 ] ))** 3
				if(val > maxVal):
					maxVal = val
					maxRegion = region
	# pour cette région on prend le meilleur point
	if(maxRegion != None):
		maxVal = -math.inf
		maxGroup = None
		groups = maxRegion.getGroups()
		for row in groups:
			for group in row:
				if(group.getScore() == 0 or (group.positionX == 0 and group.positionY == 0)):
					val = -math.inf
				else:
					val = group.getScore()*2 - group.getPoids()
					if(val > maxVal):
						maxVal = val
						maxGroup = group

		print("---",secondes,",",maxVal, "(",maxGroup.positionX,",",maxGroup.positionY,") ->",[str(cadeau) for cadeau in maxGroup.cadeaux])

		cheminAller = chemin(groupe(0,0),maxGroup,traineau(reachRange,Accelerationcalculator))
		cheminAller.move()
		cheminRetour = chemin(maxGroup,groupe(0,0),traineau(reachRange,Accelerationcalculator))
		cheminRetour.move()

		bcl = boucle()
		bcl.chemins = [cheminAller,cheminRetour]
		carrotCount = bcl.getCarotteConsommes()
		if(carrotCount > 0):
			bcl.loadingActions = [["LoadCarrots",carrotCount]]
		for cadeau in maxGroup.cadeaux:
			if(not cadeau.delivre):
				bcl.loadingActions.append(["LoadGift",cadeau.nom])
				cadeau.delivre = True

		#print(str(bcl))
		if(secondes - bcl.getTempsConsomme() >= 0):
			parcoursFinal.boucles.append(bcl)
			secondes = secondes - bcl.getTempsConsomme()

print("----------------")
print(len(str(parcoursFinal)))
with open("test.out.txt", 'w') as a_fichier:
        contenu = a_fichier.write(str(parcoursFinal))