import os
import sys
import inspect
from scipy.spatial import distance
import math

challenge = "b_better_hurry.in.txt"

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from model import cadeau,groupe, heatMap, chemin, boucle, parcoursFinal,traineau,accelerationCalculator
import fileParser

(cadeaux, secondes, reachRange, accCalculator) = fileParser.parseChallenge(challenge)

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
				val = region.getPoids() * -20 + region.getScore()*100 -(distance.euclidean([0,0],[(region.maxX + region.minX) / 2, (region.maxY + region.minY) / 2 ] )//15)** 2
				if(val > maxVal):
					maxVal = val
					maxRegion = region
	# pour cette région on prend le meilleur point
	if(maxRegion != None):
		maxVal = -math.inf
		maxGroup = groupe(0,0)
		groups = maxRegion.getGroups()
		for row in groups:
			for group in row:
				score = group.getScore()
				accCalculator.updatePoids(group.getPoids() + 8)
				if(score == 0 or (group.positionX == 0 and group.positionY == 0)):
					val = -math.inf
				else:
					val = score*10 - group.getPoids()*2
					if(val > maxVal):
						maxVal = val
						maxGroup = group
		
		print("---",secondes,",",maxVal, "(",maxGroup.positionX,",",maxGroup.positionY,") ->",maxGroup.getScore())# [str(cadeau) for cadeau in maxGroup.cadeaux])
		accCalculator.updatePoids(maxGroup.getPoids() + 8) # on ajoute +8 pour représenter le pire cas possible d'utilisation de carottes, sujet a changement
		cheminAller = chemin(groupe(0,0),maxGroup,reachRange,accCalculator)
		cheminAller.move()
		accCalculator.updatePoids(4) # on ajoute +8 pour représenter le pire cas possible d'utilisation de carottes, sujet a changement
		cheminRetour = chemin(maxGroup,groupe(0,0),reachRange,accCalculator)
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
print(secondes)
with open("test.out.txt", 'w') as a_fichier:
        contenu = a_fichier.write(str(parcoursFinal))

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import scorer
print(scorer.score(challenge,"test.out.txt"))