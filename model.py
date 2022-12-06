from typing import Literal
from scipy.spatial import distance


class accelerationCalculator():
	"""
	classe permettant de déterminer l'accélération maximale a partir d'un profil d'accélération
	"""

	def __init__(self,ranges: list[list[int]]) -> None:
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
		self.ranges = ranges

	def getMaxAcceleration(self,poids: int) -> int:
		"""
		Retourne l'accélération maximale possible pour un poids donné par rapport a un certain profil d'accélération

		Args:
			poids (int): le poids du traineau pour lequel l'on doit calculer l'accélération maximale possible

		Returns:
			int: l'accélération maximale possible pour ce trainneau
		"""
		for range in self.config:
			if(poids <= range[0] ):
				return range[1]
		return 0

class rangeCalculator:
	"""
	classe permettant de déterminer si une case est 
	"""

	def __init__(self,reachRange: int) -> None:
		self.range = reachRange
		self.rangeMask = []
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
	def __init__(self,nom: str, poids: int, score: int, positionX: int, positionY: int) -> None:
		self.nom = nom
		self.poids = poids
		self.score = score
		self.positionX = positionX
		self.positionY = positionY
		self.delivre = False
		self.enTransport = False
		self.groupes = []  #il est impératif de ne jamais modifier directement cette liste (voir groupe.addCadeau et groupe.removeCadeau)

	def __lt__(self,other):
		# ici je définis comment comparer deux tableau comme ça on pourra les trier par poids facilement avec .sort()
		#TODO : ici on peut eventuelleement penser a ajouter un poids a la distance dans la comparaison
		return self.poids < other.poids

class groupe:
	def __init__(self, positionX: int, positionY: int) -> None:
		self.positionX = positionX
		self.positionY = positionY
		self.delivre = False
		self.cadeaux = []  #il est impératif de ne jamais modifier directement cette liste (voir groupe.addCadeau et groupe.removeCadeau)
	
	def addCadeau(self, cadeau: cadeau) -> any:
		if((cadeau not in self.cadeaux) and (self not in cadeau.groupes) ):
			self.cadeaux.append(cadeau)
			cadeau.groupes.append(self)
		else:
			raise RuntimeWarning("un meme cadeau ne peut pas etre présent deux fois dans le meme groupe")
		return self

	def removeCadeau(self, cadeau: cadeau) -> any:
		if((cadeau in self.cadeaux) and (self in cadeau.groupes) ):
			self.cadeaux.remove(cadeau)
			cadeau.groupes.remove(self)
		else:
			raise RuntimeWarning("il est impossible de retirer un cadeau d'un groupe si celui-ci n'en fait pas partie")
		return self

	def getPoids(self) -> int:
		return sum([(0 if elem.delivre else elem.poids) for elem in self.cadeaux])

	def getScore(self) -> int:
		return sum([(0 if elem.delivre else elem.score) for elem in self.cadeaux])

class heatMap():

	def __init__(self, reachRange: int, cadeaux: list[cadeau]) -> None:
		self.cadeauxMap = {}
		self.range = reachRange
		self.rangeCalculator = rangeCalculator(reachRange)
		#première boucle, on crée tout les groupes, grossièrement du O(n²), mais les dimensions restant raisonnables ça devrait etre ok
		for cadeau in cadeaux:
			self.cadeauxMap[(cadeau.positionX,cadeau.positionY)] = cadeau

	def getScore(self,x,y) -> int:
		score = 0
		for i in range(x - self.range, x + self.range):
			for j in range(y - self.range, y + self.range):
				cadeau = self.cadeauxMap.get((i,j),None)
				if(cadeau != None):
					if(self.rangeCalculator.isInRange(i,j,x,y)):
						score += cadeau.score
		return score

	def getGroupe(self,x,y) -> groupe:
		g = groupe(x,y)
		for i in range(x - self.range, x + self.range):
			for j in range(y - self.range, y + self.range):
				cadeau = self.cadeauxMap.get((i,j),None)
				if(cadeau != None):
					if(self.rangeCalculator.isInRange(i,j,x,y)):
						g.addCadeau(cadeau)
		return g

class traineau:
	def __init__(self,reachRange: int, accelerationCalculator: accelerationCalculator) -> None:
		self.positionX = 0 
		self.positionY = 0
		self.vitesseX = 0
		self.vitesseY = 0
		self.nbCarottes = 0
		self.cadeaux = []  #il est impératif de ne jamais modifier directement cette liste (voir traineau.chargerCadeau et traineau.livrerCadeau)
		self.range = reachRange
		self.rangeCalculator = rangeCalculator(reachRange)
		self.accelerationCalculator = accelerationCalculator

	def accelerer(self,quantity : int, direction : Literal["up","down","left","right"]) -> any:
		#TODO : integrer la verification de l'acceleration max par raport au chargement des cadeaux
		if(quantity > self.accelerationCalculator.getMaxAcceleration(self.getPoids())):
			if(quantity < 0):
				if(self.nbCarottes > 0):
					if(direction == "up"):
						self.vitesseY += quantity
					elif(direction == "down"):
						self.vitesseY += -quantity
					elif(direction == "left"):
						self.vitesseX += -quantity
					elif(direction == "right"):
						self.vitesseX += quantity
					self.nbCarottes += -1
				else:
					raise RuntimeWarning("il est impossible d'effectuer une acceleration sans carottes")
			else:
				raise ValueError("il est impossible d'effectuer une acceleration négative")
		else:
			raise ValueError("il est impossible d'effectuer une acceleration au dela des limites imposées par le poids du traineau. Poids actuel : " + str(self.getPoids()) + " Acceleration max : " + str(self.accelerationCalculator.getMaxAcceleration(self.getPoids())))
		return self

	def flotter(self, duration: int) -> any:
		for i in range(duration):
			self.positionX += self.vitesseX
			self.positionY += self.vitesseY
		return self
			
	def chargerCarotte(self,quantity: int) -> any:
		if(self.rangeCalculator.isInRange(self.positionX,self.positionY,0,0)):
			if((self.nbCarottes + quantity) >= 0):
				self.nbCarottes += quantity
			else:
				raise RuntimeWarning("il est impossible d'avoir une quantité négative de carottes'")
		else:
			raise RuntimeWarning("il est impossible de charger des carottes si l'on n'est pas a porté de (0,0)")
		return self
		
	def chargerCadeau(self, cadeau: cadeau) -> any:
		if(self.rangeCalculator.isInRange(self.positionX,self.positionY,0,0)):
			if(cadeau not in self.cadeaux):
				self.cadeaux.append(cadeau)
			else:
				raise RuntimeWarning("un meme cadeau ne peut pas etre chargé deux fois dans le traineau")
		else:
			raise RuntimeWarning("il est impossible de charger un cadeau si l'on n'est pas a porté de (0,0)")
		return self

	def livrerCadeau(self, cadeau: cadeau) -> any:
		if(self.rangeCalculator.isInRange(self.positionX,self.positionY,cadeau.positionX,cadeau.positionY)):
			if(cadeau in self.cadeaux):
				self.cadeaux.remove(cadeau)
				cadeau.delivre = True
				#TODO : implémenter le score
			else:
				raise RuntimeWarning("il est impossible de livrer un cadeau qui n'est pas chargé dans le trainneau")
		else:
			raise RuntimeWarning("il est impossible de charger un cadeau si l'on n'est pas a porté du point de dépot du cadeau")
		return self

	def chargerGroupe(self, groupe: groupe) -> any:
		for cadeau in groupe.cadeaux:
			if(not cadeau.delivre):
				self.chargerCadeau(cadeau)

	
	def livrerGroupe(self, groupe: groupe) -> any:
		if(self.positionX == groupe.positionX and self.positionY == groupe.positionY):
			for cadeau in groupe.cadeaux:
				if(cadeau in self.cadeaux):
					self.livrerCadeau(cadeau)
		raise RuntimeWarning("il faut se situer au coordonées exactes du groupe si l'on shouaite le livrer")
			
	def getPoids(self) -> int:
		return sum([elem.poids for elem in self.cadeaux]) + self.nbCarottes

class chemin:
	def __init__(self,begining: groupe, end: groupe) -> None:
		self.begining = begining
		self.end = end
		self.travelActions = []
		# format de self.travelActions: 
		# [
		# 	["accLeft", 8],
		# 	["float", 3],
		# 	["LoadGift", "Olivia"],
		# 	["DeliverGift", "Bob"],
		# 	["LoadCarrots", 2],
		# 	["LoadGift", "Amine"]
		# ]

		#TODO : parcours simple - calcul et création des instructions du chemin ici, possibilité d'utilise un objet Traineau

	def __str__(self) -> str:
		#TODO : sérialisation - transformation de self.TravelActions en string ICI
		pass

class boucle:
	def __init__(self) -> None:
		self.chemins = []

	def __str__(self) -> str:
		#TODO : sérialisation - transformation de self.chemins en string ICI
		pass

class parcoursFinal:
	def __init__(self) -> None:
		self.boucles = []

	def __str__(self) -> str:
		#TODO : sérialisation - transformation de self.boucles en string ICI
		pass
