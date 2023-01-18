import os
import sys
import inspect
from scipy.spatial import distance
import math

challenge = "f_festive_flyover.in.txt"

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from model import cadeau, groupe, heatMap, chemin, boucle, parcoursFinal, traineau, accelerationCalculator
import fileParser

(cadeaux, secondes, reachRange, accCalculator) = fileParser.parseChallenge(challenge)

heatmap = heatMap(reachRange, cadeaux)
parcoursFinal = parcoursFinal()
maxValRegion = 0
while (secondes > 0 and maxValRegion != -math.inf):

	# on détermine la valeur de chaque région
	# on prend la région avec la plus grande valeur
	maxValRegion = -math.inf
	maxRegion = None
	for row in heatmap.regions:
		for region in row:
			# TODO : raffiner l'algo de décision
			if (region.getScore() == 0):
				val = -math.inf
			else:
				val = region.getPoids() * -20 + region.getScore() * 100 - (distance.euclidean([0, 0], [
					(region.maxX + region.minX) / 2, (region.maxY + region.minY) / 2]) // 15) ** 2
				if (val > maxValRegion):
					maxValRegion = val
					maxRegion = region
	# pour cette région on prend le meilleur point
	if (maxRegion != None):
		bcl = boucle()
		previousGroup = groupe(0, 0)
		maxValGroupe = 0
		while (maxValGroupe != -math.inf):
			maxValGroupe = -math.inf
			maxGroup = groupe(0, 0)
			groups = maxRegion.getGroups()
			for row in groups:
				for group in row:
					score = group.getScore()
					if (score == 0 or (group.positionX == 0 and group.positionY == 0) or group.delivre == True):
						val = -math.inf
					else:
						val = score * 10 - group.getPoids() * 2
						if (val > maxValGroupe):
							maxValGroupe = val
							maxGroup = group

			cheminRetour = chemin(maxGroup, previousGroup, reachRange, accCalculator, bcl.getPoids())
			cheminAller = chemin(groupe(0, 0), maxGroup, reachRange, accCalculator,
								 bcl.getPoids() + cheminRetour.carotteConsommes + maxGroup.getPoids())

			# print(str(bcl))
			if (secondes - (
					bcl.getTempsConsomme() + cheminRetour.tempsConsomme + cheminAller.tempsConsomme) >= 0 and maxValGroupe != -math.inf):
				previousGroup = maxGroup
				if (len(bcl.chemins) != 0):
					pop = bcl.chemins.pop(0)
				bcl.chemins.insert(0, cheminRetour)
				bcl.chemins.insert(0, cheminAller)
				for cadeau in maxGroup.cadeaux:
					if (not cadeau.enTransport):
						cadeau.enTransport = True
			else:
				maxGroup.delivre = True
				for cadeau in maxGroup.cadeaux:
					cadeau.delivre = True

		print("---", secondes, bcl.getPoids(), bcl.getScore(), len(bcl.chemins))
		if (secondes - bcl.getTempsConsomme() >= 0):
			parcoursFinal.boucles.append(bcl)
			secondes = secondes - bcl.getTempsConsomme()
			lastGroup = groupe(0, 0)
			for c in bcl.chemins:
				# print("(",c.begining.positionX,c.begining.positionY,")->(",c.end.positionX,c.end.positionY,")")
				if (c.begining.positionX != lastGroup.positionX or c.begining.positionY != lastGroup.positionY):
					raise RuntimeWarning("chemin non cohérent")
				lastGroup = c.end
				c.move()
				for cadeau in c.end.cadeaux:
					if (not cadeau.delivre):
						bcl.loadingActions.append(["LoadGift", cadeau.nom])
						# print(str(cadeau),end="")
						cadeau.delivre = True
			carrotCount = bcl.getCarotteConsommes()
			if (carrotCount > 0):
				bcl.loadingActions.append(["LoadCarrots", carrotCount])
		else:
			for c in bcl.chemins:
				c.move()
				for cadeau in c.end.cadeaux:
					cadeau.delivre = True

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

print(scorer.score(challenge, "test.out.txt"))
