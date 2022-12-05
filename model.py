from typing import Literal, Self
from scipy.spatial import distance

def isInRange(originX : int, originY : int, range: int, targetX : int, targetY : int) -> bool:
	#ici j'utilise scipy car c'est une opération qui va etre répété très souvent et elle a bien interret a etre optimisé comme jaja
	return distance.euclidean([originX,originY],[targetX,targetY]) <= range


class cadeau(object):
	def __init__(self,nom: str, poids: int, positionX: int, positionY: int) -> None:
		self.nom = nom
		self.poids = poids
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
	
	def addCadeau(self, cadeau: cadeau) -> Self:
		if((cadeau not in self.cadeaux) and (self not in cadeau.groupes) ):
			self.cadeaux.append(cadeau)
			cadeau.groupes.append(self)
		else:
			raise RuntimeWarning("un meme cadeau ne peut pas etre présent deux fois dans le meme groupe")
		return self

	def removeCadeau(self, cadeau: cadeau) -> Self:
		if((cadeau in self.cadeaux) and (self in cadeau.groupes) ):
			self.cadeaux.remove(cadeau)
			cadeau.groupes.remove(self)
		else:
			raise RuntimeWarning("il est impossible de retirer un cadeau d'un groupe si celui-ci n'en fait pas partie")
		return self

	def getPoids(self) -> int:
		return sum([(0 if elem.delivre else elem.poids) for elem in self.cadeaux])


class heatMap:
	def __init__(self, width: int, height: int, reachRange: int, cadeaux: list[cadeau]) -> None:
		self.heatMap = []
		#TODO : faire de l'optimisation vénère sur cette fonction, pas question de faire du O(n⁴)
		for i in range(width):
			self.heatMap[i] = []
			for j in range(height):
				self.heatMap[i][j] = groupe(i,j)
				for cadeau in cadeaux:
					if(isInRange(i,j,reachRange,cadeau.positionX,cadeau.positionY)):
						self.self.heatMap[i][j].addCadeau(cadeau)
		

	def getGroupe(self,x,y) -> groupe:
		return self.heatMap[x][y]

class traineau:
	def __init__(self,reachRange: int) -> None:
		self.positionX = 0 
		self.positionY = 0
		self.vitesseX = 0
		self.vitesseY = 0
		self.nbCarottes = 0
		self.cadeaux = []  #il est impératif de ne jamais modifier directement cette liste (voir traineau.chargerCadeau et traineau.livrerCadeau)
		self.range = reachRange
		self.accelerationUpperBound = 4

	def accelerer(self,quantity : int, direction : Literal["up","down","left","right"]) -> Self:
		#TODO : integrer la verification de l'acceleration max par raport au chargement des cadeaux
		if(quantity > self.accelerationUpperBound):
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
			raise ValueError("il est impossible d'effectuer une acceleration au dela des limites imposées par le poids du traineau. Poids actuel : " + str(self.getPoids()) + " Acceleration max : " + str(self.accelerationUpperBound))
		return self

	def flotter(self, duration: int) -> Self:
		for i in range(duration):
			self.positionX += self.vitesseX
			self.positionY += self.vitesseY
		return self
			
	def chargerCarotte(self,quantity: int) -> Self:
		if(isInRange(self.positionX,self.positionY,self.range,0,0)):
			if((self.nbCarottes + quantity) >= 0):
				self.nbCarottes += quantity
				self.updatePoids()
			else:
				raise RuntimeWarning("il est impossible d'avoir une quantité négative de carottes'")
		else:
			raise RuntimeWarning("il est impossible de charger des carottes si l'on n'est pas a porté de (0,0)")
		return self
		
	def chargerCadeau(self, cadeau: cadeau) -> Self:
		if(isInRange(self.positionX,self.positionY,self.range,0,0)):
			if(cadeau not in self.cadeaux):
				self.cadeaux.append(cadeau)
				self.updatePoids()
			else:
				raise RuntimeWarning("un meme cadeau ne peut pas etre chargé deux fois dans le traineau")
		else:
			raise RuntimeWarning("il est impossible de charger un cadeau si l'on n'est pas a porté de (0,0)")
		return self

	def livrerCadeau(self, cadeau: cadeau) -> Self:
		if(isInRange(self.positionX,self.positionY,self.range,cadeau.positionX,cadeau.positionY)):
			if(cadeau in self.cadeaux):
				self.cadeaux.remove(cadeau)
				cadeau.delivre = True
				self.updatePoids()
				#TODO : implémenter le score
			else:
				raise RuntimeWarning("il est impossible de livrer un cadeau qui n'est pas chargé dans le trainneau")
		else:
			raise RuntimeWarning("il est impossible de charger un cadeau si l'on n'est pas a porté du point de dépot du cadeau")
		return self

	def chargerGroupe(self, groupe: groupe) -> Self:
		for cadeau in groupe.cadeaux:
			if(not cadeau.delivre):
				self.chargerCadeau(cadeau)

	
	def livrerGroupe(self, groupe: groupe) -> Self:
		if(self.positionX == groupe.positionX and self.positionY == groupe.positionY):
			for cadeau in groupe.cadeaux:
				if(cadeau in self.cadeaux):
					self.livrerCadeau(cadeau)
		raise RuntimeWarning("il faut se situer au coordonées exactes du groupe si l'on shouaite le livrer")

	def updatePoids(self) -> Self:
		poids = self.getPoids()
		if(poids <= 30):
			self.accelerationUpperBound = 4
		elif(poids <= 500):
			self.accelerationUpperBound = 2
		else:
			self.accelerationUpperBound = 0
			
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
