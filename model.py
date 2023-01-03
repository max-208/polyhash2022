from __future__ import annotations
from typing import Literal
from scipy.spatial import distance
import math
from tkinter import *

class accelerationCalculator:
	"""
	classe permettant de déterminer l'accélération maximale a partir d'un profil d'accélération
	"""

	def __init__(self, ranges: list[list[int]]) -> None:
		"""
		Args:
			ranges (list[list[int]]): liste contenant des listes de deux éléments, \n
				le premier element est le poids maximal de ce profil d'accélération,\n
				le second element est l'accélération maximale possible via ce profil d'accélération
		"""
		# structure :
		# [			/!\ l'ordre des elements est important
		#	[10,4],	-> de 0 a 10kg, acceleration max de 4
		#	[20,2],	-> de 11 a 20kg, acceleration max de 2
		#	[50,1]	-> de 21 a 50kg, acceleration max de 1
		# ]			-> au dela de 51kg, acceleration max de 0
		self.ranges:list[list[int]] = ranges
		self.currentMaxAcceleration = self.ranges[0][1]

	def getMaxAcceleration(self) -> int:
		"""
		Retourne l'accélération maximale possible pour par rapport a un certain profil d'accélération et au poids mis a jour par updatePoids

		Returns:
			int: l'accélération maximale possible pour ce trainneau
		"""
		return self.currentMaxAcceleration

	def updatePoids(self,poids: int) -> any:
		"""
		met a jour l'accélération maximale du traineau

		Args:
			poids (int): le poids du traineau pour lequel l'on doit calculer l'accélération maximale possible

		Returns:
			accelerationCalculator: soi-meme
		"""
		for range in self.ranges:
			if(poids <= range[0] ):
				self.currentMaxAcceleration = range[1]
				return self
		self.currentMaxAcceleration = 0
		return self


class rangeCalculator:
	"""
	classe permettant de déterminer si une case est
	"""

	def __init__(self,reachRange: int) -> None:
		self.range = reachRange
		self.rangeMask:list[list[bool]] = []
		for i in range(reachRange*2 + 1):
			row = []
			for j in range(reachRange*2 + 1):
				row.append((distance.euclidean([reachRange,reachRange],[i,j]) <= reachRange))
			self.rangeMask.append(row)

	def isInRange(self, originX : int, originY : int, targetX : int, targetY : int) -> bool:
		"""
		méthode utile permettant de valider ou non si une case est accessible d'une autre

		Args:
			originX (int): coordonée x de la case d'origine
			originY (int): coordonée y de la case d'origine
			targetX (int): coordonée x de la case objectif
			targetY (int): coordonée y de la case objectif

		Returns:
			bool: vrai si l'objectif est a une distance inférieure de la porté de l'origine
		"""
		x = (targetX - originX) + self.range
		y = (targetY - originY) + self.range
		if(x >= 0 and x <= self.range*2 and y >= 0 and y <= self.range*2):
			return self.rangeMask[x][y]
		return False

		#ici j'utilise scipy car c'est une opération qui va etre répété très souvent et elle a bien interret a etre optimisé comme jaja
		#return distance.euclidean([originX,originY],[targetX,targetY]) <= range


class cadeau:
	"""
	classe représentant les cadeaux et les informations qui leur sont associés : endroit de livraison, poids, score, ainsi que des informations sur son statut de transport
	"""

	def __init__(self,nom: str, poids: int, score: int, positionX: int, positionY: int) -> None:
		"""
		Args:
			nom (str): nom du récipient du cadeau
			poids (int): poids du cadeau
			score (int): score du cadeau
			positionX (int): position en x du point de livraison du cadeau
			positionY (int): position en y du point de livraison du cadeau
		"""
		self.nom = nom
		self.poids = poids
		self.score = score
		self.positionX = positionX
		self.positionY = positionY
		self.delivre = False
		self.enTransport = False

	def __str__(self) -> str:
		return "(" + self.nom + ", " + str(self.poids) + "kg, " + str(self.score) + "pts, <" + str(self.positionX) + "," + str(self.positionY) + ">, " + str(self.delivre) + ", " + str(self.delivre) +")"

	def __lt__(self,other):
		# ici je définis comment comparer deux tableau comme ça on pourra les trier par poids facilement avec .sort()
		#TODO : ici on peut eventuelleement penser a ajouter un poids a la distance dans la comparaison
		return self.poids < other.poids


class groupe:
	"""
	classe représentant les "groupes" de cadeaux,
	c'est a dire un point a partir duquel il est possible de délivrer plusieurs cadeau d'un coup
	il existe pour chaque pixel de la grille un groupe, chacun accedant à un certain nombre de cadeaux
	"""
	def __init__(self, positionX: int, positionY: int) -> None:
		"""

		Args:
			positionX (int): position en x du groupe
			positionY (int): position en y du groupe
		"""
		self.positionX = positionX
		self.positionY = positionY
		self.delivre = False
		self.cadeaux:list[cadeau] = []  #il est impératif de ne jamais modifier directement cette liste (voir groupe.addCadeau et groupe.removeCadeau)

	def addCadeau(self, cadeau: cadeau) -> any:
		"""
		Insère un cadeau dans un groupe

		Args:
			cadeau (cadeau): le cadeau a ajouter

		Raises:
			RuntimeWarning: si un cadeau est inséré deux fois dans le meme groupe

		Returns:
			groupe: lui-meme
		"""
		if((cadeau not in self.cadeaux)):
			self.cadeaux.append(cadeau)
		else:
			raise RuntimeWarning("un meme cadeau ne peut pas etre présent deux fois dans le meme groupe")
		return self

	def removeCadeau(self, cadeau: cadeau) -> any:
		"""
		retire un cadeau du groupe

		Args:
			cadeau (cadeau): le cadeau a retirer

		Raises:
			RuntimeWarning: si un cadeau retiré n'etait pas dans le groupe

		Returns:
			groupe: lui-meme
		"""
		if((cadeau in self.cadeaux) ):
			self.cadeaux.remove(cadeau)
		else:
			raise RuntimeWarning("il est impossible de retirer un cadeau d'un groupe si celui-ci n'en fait pas partie")
		return self

	def getPoids(self) -> int:
		"""
		retourne le poids du groupe (somme cummulée du poids de tout les cadeaux accesibles via ce groupe)

		Returns:
			int: poids du groupe
		"""
		return sum([(0 if elem.delivre else elem.poids) for elem in self.cadeaux])

	def getScore(self) -> int:
		"""
		retourne le score du groupe (somme cummulée du score de tout les cadeaux accesibles via ce groupe)

		Returns:
			int: score du groupe
		"""
		return sum([(0 if elem.delivre else elem.score) for elem in self.cadeaux])


class region():
	"""
	Une région représente une "section" de la heatMap d'une certaine taille,
	l'objectif de cette classe est de rapidement avoir une information sur une zone
	pour en déterminer la valeur avant d'y lancer une recherche précise
	"""
	def __init__(self,width:int,minX:int,maxX:int,minY:int,maxY:int,rangeCalculator:rangeCalculator) -> None:
		"""

		Args:
			width (int): largeur et hauteur de la région (elles sont toujours carrées)
			minX (int): coordonée x minimale incluse dans la région
			maxX (int): coordonée x maximale incluse dans la région
			minY (int): coordonée y minimale incluse dans la région
			maxY (int): coordonée y maximale incluse dans la région
			rangeCalculator (rangeCalculator): l'objet permettant le calcul des portées
		"""
		self.minX = minX
		self.maxX = maxX
		self.minY = minY
		self.maxY = maxY
		self.width = width
		self.range = rangeCalculator.range
		self.rangeCalculator = rangeCalculator
		self.cadeaux:list[cadeau] = []

	def addCadeau(self,cadeau: cadeau) -> any:
		"""
		ajoute un cadeau a une région

		Args:
			cadeau (cadeau): cadeau a ajouter

		Returns:
			region: soi-meme
		"""
		self.cadeaux.append(cadeau)
		return self

	def getPoids(self) -> int:
		"""
		retourne rapidement le poids global de la région
		(somme des poids individuels de tout les cadeaux de la région)

		Returns:
			int: poids global de la région
		"""
		return sum([(0 if elem.delivre else elem.poids) for elem in self.cadeaux])

	def getScore(self) -> int:
		"""
		retourne rapidement le score global de la région
		(somme des score individuels de tout les cadeaux de la région)

		Returns:
			int: score global de la région
		"""
		return sum([(0 if elem.delivre else elem.score) for elem in self.cadeaux])

	def getGroups(self) -> list[list[groupe]]:
		"""
		génère un tableau 2D contenant tout les groupes de cette région

		Returns:
			list[list[groupe]]: un tableau 2D contenant tout les groupes de cette région
		"""
		# on crées les groupes vides
		ret = []
		for x in range(self.width):
			row = []
			for y in range(self.width):
				row.append(groupe(x + self.minX,y + self.minY))
			ret.append(row)

		# on associes les cadeaux aux groupes
		for cadeau in self.cadeaux:
			for i in range(cadeau.positionX - self.range, cadeau.positionX + self.range + 1):
				for j in range(cadeau.positionY - self.range, cadeau.positionY + self.range + 1):
					if(i-self.minX >= 0 and i-self.minX < self.width and j-self.minY >= 0 and j-self.minY < self.width ):
						if(self.rangeCalculator.isInRange(cadeau.positionX,cadeau.positionY,i,j)):
							#print(self.width,i,j,i-self.minX,j-self.minY)
							ret[i-self.minX][j-self.minY].addCadeau(cadeau)

		return ret


class heatMap:
	"""
	classe représentant une "heatmap" soit une carte globale contenant des régions qui elles meme contiennent des groupes
	"""

	def __init__(self, reachRange: int, cadeaux: list[cadeau]) -> None:
		"""

		Args:
			reachRange (int): portée a partir de laquelle il est possible d'accéder au cadeaux
			cadeaux (list[cadeau]): liste des cadeaux contenus dans cette heatmap
		"""
		self.regions:list[list[region]] = []
		self.range = reachRange
		self.rangeCalculator = rangeCalculator(reachRange)
		self.cadeaux = {}
		# on détecte les limites
		minX = math.inf
		minY = math.inf
		maxX = -math.inf
		maxY = -math.inf
		for cadeau in cadeaux:
			self.cadeaux[cadeau.nom] = cadeau
			minX = cadeau.positionX if cadeau.positionX < minX else minX
			minY = cadeau.positionY if cadeau.positionY < minY else minY
			maxX = cadeau.positionX if cadeau.positionX > maxX else maxX
			maxY = cadeau.positionY if cadeau.positionY > maxY else maxY

		width = maxX - minX
		height = maxY - minY

		self.regionSize = 10 + width//100 # TODO: a fine tune, taille en cases d'un bloc "région"

		self.offsetX = minX
		self.offsetY = minY

		#on crées les régions en accordance
		for i in range(width//self.regionSize+1):
			row = []
			for j in range(height//self.regionSize+1):
				newMinX = minX + i * self.regionSize
				newMinY = minY + j * self.regionSize
				row.append(region(self.regionSize,newMinX,newMinX + self.regionSize,newMinY, newMinY + self.regionSize, self.rangeCalculator ))
			self.regions.append(row)

		# on y ajoutes les cadeaux
		for cadeau in cadeaux:
			self.regions[(cadeau.positionX-self.offsetX)//self.regionSize][(cadeau.positionY-self.offsetY)//self.regionSize].addCadeau(cadeau)

	def display(self):
		rectangleSize = 10
		window = Tk()
		width = len(self.regions)
		height = len(self.regions[0])
		heatmap = Canvas(window, width=width*rectangleSize, height=height*rectangleSize)
		heatmap.pack()
		rowIndex = 0
		minPoids = math.inf
		maxPoids = -math.inf
		data = []
		for i in self.regions:
			columnIndex = 0
			for j in i:
				poids = j.getPoids()
				data.append((rowIndex, columnIndex, poids))
				if poids > maxPoids:
					maxPoids = poids
				elif poids < minPoids:
					minPoids = poids
				columnIndex += rectangleSize
			rowIndex += rectangleSize
		dataSize = len(data)
		for i in range(dataSize):
			proportion = int((data[i].__getitem__(2)/(maxPoids-minPoids))*255)
			color = "#%02x%02x%02x" % (255-proportion, 255-proportion, 255-proportion)
			rowIndex = data[i].__getitem__(0)
			columnIndex = data[i].__getitem__(1)
			heatmap.create_rectangle(rowIndex, columnIndex, rowIndex + rectangleSize + 1,columnIndex + rectangleSize + 1, fill=color, outline=color)
		heatmap.create_rectangle(-self.offsetX//self.regionSize*rectangleSize, -self.offsetY//self.regionSize*rectangleSize, -self.offsetX//self.regionSize*rectangleSize + rectangleSize + 1, -self.offsetY//self.regionSize*rectangleSize + rectangleSize + 1, fill='', outline='red')
		mainloop()


class traineau:
	"""
	classe représentant le traineau du pere noel, a pour but de simuler ses déplacements a la fois pour le solver et le scorer
	"""
	def __init__(self,reachRange: int, accelerationCalculator: accelerationCalculator) -> None:
		"""

		Args:
			reachRange (int): portée a partir de laquelle il est possible d'accéder au cadeaux
			accelerationCalculator (accelerationCalculator): courbe d'accélération du pere noel
		"""
		self.positionX = 0
		self.positionY = 0
		self.vitesseX = 0
		self.vitesseY = 0
		self.nbCarottes = 0
		self.cadeaux:list[cadeau] = []  #il est impératif de ne jamais modifier directement cette liste (voir traineau.chargerCadeau et traineau.livrerCadeau)
		self.range = reachRange
		self.poids = 0
		self.rangeCalculator = rangeCalculator(reachRange)
		self.accelerationCalculator = accelerationCalculator
		self.ignoreCarottes = False

	def accelerer(self,quantity : int, direction : Literal["up","down","left","right"]) -> any:
		"""
		accelere le pere noel dans une direction

		Args:
			quantity (int): accélération en m/s a rajouter
			direction (&quot;up&quot;,&quot;down&quot;,&quot;left&quot;,&quot;right&quot;): direction de l'accélération

		Raises:
			RuntimeWarning: si on accelere sans carottes
			ValueError: si on effectue une accélération négative
			ValueError: si on effectue une accélération plus haute que l'accélération max

		Returns:
			traineau: soi-meme
		"""
		if(quantity <= self.accelerationCalculator.getMaxAcceleration()):
			if(quantity >= 0):
				if(self.nbCarottes > 0 or self.ignoreCarottes):
					if(direction == "up"):
						self.vitesseY += quantity
					elif(direction == "down"):
						self.vitesseY += -quantity
					elif(direction == "left"):
						self.vitesseX += -quantity
					elif(direction == "right"):
						self.vitesseX += quantity
					if(not self.ignoreCarottes):
						self.nbCarottes += -1
						self.poids += -1
				else:
					raise RuntimeWarning("il est impossible d'effectuer une acceleration sans carottes")
			else:
				raise ValueError("il est impossible d'effectuer une acceleration négative")
		else:
			raise ValueError("il est impossible d'effectuer une acceleration au dela des limites imposées par le poids du traineau. Poids actuel : " + str(self.getPoids()) + " Acceleration max : " + str(self.accelerationCalculator.getMaxAcceleration()))
		return self

	def flotter(self, duration: int) -> any:
		"""
		classe faisant passer le temps, la position du traineau change selon sa vélocité actuelle

		Args:
			duration (int): durée en seconde a flotter

		Returns:
			traineau: soi-meme
		"""
		if(duration <= 0):
			raise RuntimeWarning("impossible d'effectuer un float de durée 0 ou négative")
		for i in range(duration):
			self.positionX += self.vitesseX
			self.positionY += self.vitesseY
		return self

	def chargerCarotte(self,quantity: int) -> any:
		"""
		charge une ou plus carotte sur le pere noel

		Args:
			quantity (int): quantité de carottes a charger

		Raises:
			RuntimeWarning: si l'on est trop loins de (0,0) pour charger des carottes
			RuntimeWarning: si l'on essaie de retirer plus de carottes que n'en contient le traineau

		Returns:
			any: _description_
		"""
		if(self.rangeCalculator.isInRange(self.positionX,self.positionY,0,0)):
			if((self.nbCarottes + quantity) >= 0):
				self.nbCarottes += quantity
				self.poids += quantity
				self.accelerationCalculator.updatePoids(self.getPoids())
			else:
				raise RuntimeWarning("il est impossible d'avoir une quantité négative de carottes'")
		else:
			raise RuntimeWarning("il est impossible de charger des carottes si l'on n'est pas a porté de (0,0)")
		return self

	def chargerCadeau(self, cadeau: cadeau) -> any:
		"""
		charge un cadeau sur le traineau

		Args:
			cadeau (cadeau): le cadeau a charger

		Raises:
			RuntimeWarning: si l'on est trop loin de (0,0) pour charger un cadeau
			RuntimeWarning: si le cadeau est déja dans le traineau

		Returns:
			traineau: soi-meme
		"""
		if(self.rangeCalculator.isInRange(self.positionX,self.positionY,0,0)):
			if(cadeau not in self.cadeaux):
				self.cadeaux.append(cadeau)
				self.poids += cadeau.poids
				self.accelerationCalculator.updatePoids(self.getPoids())
			else:
				raise RuntimeWarning("un meme cadeau ne peut pas etre chargé deux fois dans le traineau")
		else:
			raise RuntimeWarning("il est impossible de charger un cadeau si l'on n'est pas a porté de (0,0)")
		return self

	def livrerCadeau(self, cadeau: cadeau) -> any:
		"""
		livre un cadeau a son lieu d'arrivée défini

		Args:
			cadeau (cadeau): le cadeau a livrer

		Raises:
			RuntimeWarning: si l'on est trop loin du point de dépot du cadeau pour livrer
			RuntimeWarning: si on essaie de livrer un cadeau qui n'est pas sur le traineau

		Returns:
			traineau: soi-meme
		"""
		if(self.rangeCalculator.isInRange(self.positionX,self.positionY,cadeau.positionX,cadeau.positionY)):
			if(cadeau in self.cadeaux):
				self.cadeaux.remove(cadeau)
				self.poids += -cadeau.poids
				self.accelerationCalculator.updatePoids(self.getPoids())
				cadeau.delivre = True
			else:
				raise RuntimeWarning("il est impossible de livrer un cadeau qui n'est pas chargé dans le traineau : " + str(cadeau))
		else:
			raise RuntimeWarning("il est impossible de livrer un cadeau si l'on n'est pas a porté du point de dépot du cadeau : " + str(cadeau))
		return self

	def chargerGroupe(self, groupe: groupe) -> any:
		"""
		charge un groupe entier de cadeau sur le trainneau

		Args:
			groupe (groupe): le groupe a charger

		Returns:
			traineau: soi-meme
		"""
		for cadeau in groupe.cadeaux:
			if(not cadeau.delivre):
				self.chargerCadeau(cadeau)
		return self


	def livrerGroupe(self, groupe: groupe) -> any:
		"""
		livre un groupe entier de cadeaux

		Args:
			groupe (groupe): le groupe a livrer

		Raises:
			RuntimeWarning: si le traineau n'est pas sur la position exacte du groupe

		Returns:
			traineau: soi-meme
		"""
		if(self.positionX == groupe.positionX and self.positionY == groupe.positionY):
			for cadeau in groupe.cadeaux:
				if(cadeau in self.cadeaux):
					self.livrerCadeau(cadeau)
		else:
			raise RuntimeWarning("il faut se situer au coordonées exactes du groupe si l'on shouaite le livrer")
		return self


	def getPoids(self) -> int:
		"""
		retourne le poids chargé sur le traineau

		Returns:
			int: le poids chargé
		"""
		return self.poids
		#return sum([elem.poids for elem in self.cadeaux]) + self.nbCarottes

class chemin:
	"""
	classe représentant un chemin, un chemin est une suite d'actions représentant un mouvement
	"""
	def __init__(self,begining: groupe, end: groupe, reachRange : int = 0, accelerationCalculator : accelerationCalculator = None) -> None:
		self.begining = begining
		self.end = end
		self.travelActions:list[list[str|int]] = []
		# format de self.travelActions:
		# [
		# 	["AccLeft", 8],
		# 	["float", 3],
		# 	["LoadGift", "Olivia"],
		# 	["DeliverGift", "Bob"],
		# 	["LoadCarrots", 2],
		# 	["LoadGift", "Amine"]
		# ]
		self.reachRange = reachRange
		self.tempsConsomme = 0
		self.carotteConsommes = 0
		self.accelerationCalculator = accelerationCalculator
		self.traineau = traineau(self.reachRange,self.accelerationCalculator)
		#Distance relative entre le point initial et le point destination
		self.delta_x: int = end.positionX - begining.positionX 		#delta_x corresponds à la distance relative en C
		self.delta_y: int = end.positionY - begining.positionY		#delta_y corresponds à la distance relative en R

	def move(self):
		self.traineau.positionX = self.begining.positionX
		self.traineau.positionY = self.begining.positionY
		self.traineau.ignoreCarottes = True
		self.travelActions = []
		self.carotteConsommes = 0
		self.tempsConsomme = 0
		if(self.accelerationCalculator.getMaxAcceleration() <= 0):
			self.tempsConsomme = -math.inf
			return

		# calcul de l'accélération maximale possible permettant d'arriver a point + l'éventuel rattrapage a effectuer
		acc = self.accelerationCalculator.getMaxAcceleration()

		self.stepAccelerationX = acc if acc < abs(self.delta_x) else abs(self.delta_x)
		self.stepAccelerationY = acc if acc < abs(self.delta_y) else abs(self.delta_y)

		self.catchupX = abs(self.delta_x)%acc if acc < abs(self.delta_x) else 0
		self.catchupY = abs(self.delta_y)%acc if acc < abs(self.delta_y) else 0

		# calcul du nombre d'étapes nécéssaires pour s'aligner avec la coordonnée de l'objectif en allant a la vitesse calculée ci-dessus
		tempsX = math.dist([self.begining.positionX],[self.end.positionX])//self.stepAccelerationX if self.stepAccelerationX > 0 else 0
		tempsY = math.dist([self.begining.positionY],[self.end.positionY])//self.stepAccelerationY if self.stepAccelerationY > 0 else 0

		# mouvement évident (ne pas bouger)
		if(self.begining.positionX == self.end.positionX and self.begining.positionY == self.end.positionY):
			pass

		# mouvements évidents (lignes droites)
		#
		#   a v
		#   |           >      <
		#   .      et  a -- . -- b
		#   |
		#   b ^
		#
		elif(self.begining.positionX == self.end.positionX):
			#print("Y")
			# alignement sur l'axe Y
			self.lineY()
		elif(self.begining.positionY == self.end.positionY):
			#print("X")
			# alignement sur l'axe X
			self.lineX()

		#mouvement proches (distance manhattan de - de 3 fois l'acceleration max)
		#
		#   v a                   v a
		#     |              et     |
		#   ^ . -- . -- b         ^ . -- b
		#      >        <            >  <
		#
		else: #elif(abs(self.delta_x)/self.stepAccelerationX + abs(self.delta_y)/self.stepAccelerationY <= 3):
			#print("L")
			# alignement sur l'axe Y
			self.lineY()
			# alignement sur l'axe X
			self.lineX()
		""" on met temporairement de coté les parcours composés, trop difficile a développer actuellement pour une v3
		#mouvements restants : cas combinés
		elif( tempsY > tempsX):
			#print("YS")
			# cas vertical
			#
			#      b v
			#      |
			#      . <
			#     /
			#    .
			#   /
			#  . >
			#  |
			#  .
			#  |
			#  a ^
			#

			# impulsion en Y
			self.acceleration_y(self.stepAccelerationY,1)

			# impulsion puis deceleration en X
			self.lineX()

			# flotter jusqu'a la fin
			dist =  (abs(self.end.positionY - self.traineau.positionY) // self.stepAccelerationY) - 1
			print("dist", dist)
			if( dist > 0 ):
				self.traineau.flotter(dist)
				self.travelActions.append(["Float",dist])
				self.tempsConsomme += dist

			# ralentissement partiel
			self.ralentissement_y(self.stepAccelerationY-self.catchupY,1)

			#ralentissement total (si ajustements nécéssaires)
			if(self.catchupY != 0):
				self.ralentissement_y(self.catchupY,1)

		elif(tempsY < tempsX):
			#print("XS")
			# cas horizontal
			#                    <
			#             v  . -- b
			#               /
			#              .
			#   >       ^ /
			#  a -- . -- .
			#

			#impulsion en X
			self.acceleration_x(self.stepAccelerationX,1)

			# impulsion puis deceleration en Y
			self.lineY()

			# flotter jusqu'a la fin
			dist = (abs(self.end.positionX - self.traineau.positionX) // self.stepAccelerationX) -1
			if(dist > 0):
				self.traineau.flotter(dist)
				self.travelActions.append(["Float",dist])
				self.tempsConsomme += dist

			# ralentissement partiel
			self.ralentissement_y(self.stepAccelerationY-self.catchupY,1)

			#ralentissement total (si ajustements nécéssaires)
			if(self.catchupY != 0):
				self.ralentissement_y(self.catchupY,1)

		elif(tempsY == tempsX):
			#print("DS")
			# cas diagonal
			#
			#         v b
			#           |
			#         < .
			#          /
			#         .
			#   >  ^ /
			#  a -- .
			#

			# impulsion en X
			self.acceleration_x(self.stepAccelerationX,1)

			# impulsion en Y
			self.acceleration_y(self.stepAccelerationY,1)

			# flotter pendant la zone de transition
			self.traineau.flotter(int(tempsX - 2))
			self.travelActions.append(["Float",int(tempsX - 2)])
			self.tempsConsomme += int(tempsX - 2)

			# ralentissement en X
			self.ralentissement_x(self.stepAccelerationX,1)

			# ralentissement en Y
			self.ralentissement_y(self.stepAccelerationY,1)
		"""
		# ajout des étapes de livraison des cadeaux
		for cadeau in self.end.cadeaux:
			if(not cadeau.delivre):
				self.travelActions.append(["DeliverGift", cadeau.nom])

		if(self.traineau.positionX != self.end.positionX or self.traineau.positionY != self.end.positionY):
			print("\n\n(",self.begining.positionX,self.begining.positionY,") --(",self.traineau.positionX,self.traineau.positionY,")--> (",self.end.positionX,self.end.positionY,")\n\n","delta(",self.delta_x, self.delta_y,") acc(", self.stepAccelerationX,self.stepAccelerationY,") reste(",self.catchupX,self.catchupY,") temps(", tempsX,tempsY,")\n\n", self.travelActions,"\n\n")
			raise RuntimeWarning("échec lors du décplacement, le traineau n'est pas correctement arrivé a destination")

	def lineX(self):

		intermediaryAccelerations = math.floor(math.sqrt(abs(self.delta_x)/self.stepAccelerationX))

		for i in range(intermediaryAccelerations):
			self.acceleration_x(self.stepAccelerationX,1)

		for i in range(intermediaryAccelerations-1):
			self.ralentissement_x(self.stepAccelerationX,1)

		# flotter jusqu'a la fin
		dist = (abs(self.end.positionX - self.traineau.positionX) // self.stepAccelerationX)
		if(dist > 0):
			self.traineau.flotter(dist)
			self.travelActions.append(["Float",dist])
			self.tempsConsomme += dist

		# ralentissement partiel
		self.ralentissement_x(self.stepAccelerationX - self.catchupX,1)

		#ralentissement total (si ajustements nécéssaires)
		if(self.catchupX != 0):
			self.ralentissement_x(self.catchupX, 1)


	def lineY(self):
		intermediaryAccelerations = math.floor(math.sqrt(abs(self.delta_y)/self.stepAccelerationY))

		for i in range(intermediaryAccelerations):
			self.acceleration_y(self.stepAccelerationY,1)

		for i in range(intermediaryAccelerations-1):
			self.ralentissement_y(self.stepAccelerationY,1)

		# flotter jusqu'a la fin
		dist =  (abs(self.end.positionY - self.traineau.positionY) // self.stepAccelerationY)
		if( dist > 0 ):
			self.traineau.flotter(dist)
			self.travelActions.append(["Float",dist])
			self.tempsConsomme += dist

		# ralentissement partiel
		self.ralentissement_y(self.stepAccelerationY-self.catchupY,1)

		#ralentissement total (si ajustements nécéssaires)
		if(self.catchupY != 0):
			self.ralentissement_y(self.catchupY,1)

	def acceleration_x(self,acceleration : int, numFloat: int):
			self.traineau.accelerer(acceleration, "left" if self.delta_x < 0 else "right")
			self.travelActions.append(["AccLeft" if self.delta_x < 0 else "AccRight",acceleration])
			self.carotteConsommes +=1
			self.traineau.flotter(numFloat)
			self.travelActions.append(["Float",numFloat])
			self.tempsConsomme += numFloat
			#print("acceleration x :",self.traineau.positionX, self.traineau.vitesseX)

	def ralentissement_x(self,acceleration : int, numFloat: int):
			self.traineau.accelerer(acceleration,"right" if self.delta_x < 0 else "left")
			self.travelActions.append(["AccRight" if self.delta_x < 0 else "AccLeft",acceleration])
			self.carotteConsommes +=1
			self.traineau.flotter(numFloat)
			self.travelActions.append(["Float",numFloat])
			self.tempsConsomme += numFloat
			#print("ralentissement x :", self.traineau.positionX, self.traineau.vitesseX)

	def acceleration_y(self,acceleration : int, numFloat: int):
			self.traineau.accelerer(acceleration, "down" if self.delta_y < 0 else "up")
			self.travelActions.append(["AccDown" if self.delta_y < 0 else "AccUp",acceleration])
			self.carotteConsommes +=1
			self.traineau.flotter(numFloat)
			self.travelActions.append(["Float",numFloat])
			self.tempsConsomme += numFloat
			#print("acceleration y :",self.traineau.positionY, self.traineau.vitesseY)

	def ralentissement_y(self,acceleration : int, numFloat: int):
			self.traineau.accelerer(acceleration,"up" if self.delta_y < 0 else "down")
			self.travelActions.append(["AccUp" if self.delta_y < 0 else "AccDown",acceleration])
			self.carotteConsommes +=1
			self.traineau.flotter(numFloat)
			self.travelActions.append(["Float",numFloat])
			self.tempsConsomme += numFloat
			#print("ralentissement y : ", self.traineau.positionY, self.traineau.vitesseY)

	def __str__(self) -> str:
		chemin_str = str()
		for ligne in self.travelActions:
			ligne[1] = str(ligne[1])
			chemin_str = chemin_str + '\n' +  ' '.join(ligne)
		return chemin_str



class boucle:
	"""
	classe représentant une boucle, soit un ensemble de chemins revenant au meme point d'origine
	"""
	def __init__(self) -> None:
		self.loadingActions:list[list[str|int]] = []
		self.chemins:list[chemin] = []

	def getCarotteConsommes(self):
		ret = 0
		for chemin in self.chemins:
			ret += chemin.carotteConsommes
		return ret

	def getTempsConsomme(self):
		ret = 0
		for chemin in self.chemins:
			ret += chemin.tempsConsomme
		return ret

	def __str__(self) -> str:
		boucle_str = str()
		for ligne in self.loadingActions:
			ligne[1] = str(ligne[1])
			boucle_str = boucle_str + '\n' + ' '.join(ligne)
		for element in self.chemins:
			boucle_str = boucle_str + str(element)
		return boucle_str


class parcoursFinal:
	"""
	classe représentant le parcours final, soit un ensemble de boucles
	"""
	def __init__(self) -> None:
		self.boucles:list[boucle] = []

	def __str__(self) -> str:
		"""_summary_

		Returns:
			str: _description_
		"""
		parcoursFinal_str = str()
		for element in self.boucles:
			parcoursFinal_str = parcoursFinal_str + str(element)
		size = len(parcoursFinal_str.split("\n")) - 1
		parcoursFinal_str = str(size) + parcoursFinal_str
		return parcoursFinal_str

