from typing import Literal
from scipy.spatial import distance
import math


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
        self.ranges: list[list[int]] = ranges

    def getMaxAcceleration(self, poids: int) -> int:
        """
		Retourne l'accélération maximale possible pour un poids donné par rapport a un certain profil d'accélération

		Args:
			poids (int): le poids du traineau pour lequel l'on doit calculer l'accélération maximale possible

		Returns:
			int: l'accélération maximale possible pour ce trainneau
		"""
        for range in self.config:
            if (poids <= range[0]):
                return range[1]
        return 0


class rangeCalculator:
    """
	classe permettant de déterminer si une case est
	"""

    def __init__(self, reachRange: int) -> None:
        self.range = reachRange
        self.rangeMask: list[list[bool]] = []
        for i in range(reachRange * 2 + 1):
            row = []
            for j in range(reachRange * 2 + 1):
                row.append((distance.euclidean([reachRange, reachRange], [i, j]) <= reachRange))
            self.rangeMask.append(row)

    def isInRange(self, originX: int, originY: int, targetX: int, targetY: int) -> bool:
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
        if (x >= 0 and x <= self.range * 2 and y >= 0 and y <= self.range * 2):
            return self.rangeMask[x][y]
        return False

    # ici j'utilise scipy car c'est une opération qui va etre répété très souvent et elle a bien interret a etre optimisé comme jaja
    # return distance.euclidean([originX,originY],[targetX,targetY]) <= range


class cadeau:
    def __init__(self, nom: str, poids: int, score: int, positionX: int, positionY: int) -> None:
        self.nom = nom
        self.poids = poids
        self.score = score
        self.positionX = positionX
        self.positionY = positionY
        self.delivre = False
        self.enTransport = False
        self.groupes: list[
            groupe] = []  # il est impératif de ne jamais modifier directement cette liste (voir groupe.addCadeau et groupe.removeCadeau)

    def __lt__(self, other):
        # ici je définis comment comparer deux tableau comme ça on pourra les trier par poids facilement avec .sort()
        # TODO : ici on peut eventuelleement penser a ajouter un poids a la distance dans la comparaison
        return self.poids < other.poids


class groupe:
    def __init__(self, positionX: int, positionY: int) -> None:
        self.positionX = positionX
        self.positionY = positionY
        self.delivre = False
        self.cadeaux: list[
            cadeau] = []  # il est impératif de ne jamais modifier directement cette liste (voir groupe.addCadeau et groupe.removeCadeau)

    def addCadeau(self, cadeau: cadeau) -> any:
        if ((cadeau not in self.cadeaux) and (self not in cadeau.groupes)):
            self.cadeaux.append(cadeau)
        # cadeau.groupes.append(self)
        else:
            raise RuntimeWarning("un meme cadeau ne peut pas etre présent deux fois dans le meme groupe")
        return self

    def removeCadeau(self, cadeau: cadeau) -> any:
        if ((cadeau in self.cadeaux) and (self in cadeau.groupes)):
            self.cadeaux.remove(cadeau)
            cadeau.groupes.remove(self)
        else:
            raise RuntimeWarning("il est impossible de retirer un cadeau d'un groupe si celui-ci n'en fait pas partie")
        return self

    def getPoids(self) -> int:
        return sum([(0 if elem.delivre else elem.poids) for elem in self.cadeaux])

    def getScore(self) -> int:
        return sum([(0 if elem.delivre else elem.score) for elem in self.cadeaux])


class region():
    def __init__(self, width: int, minX: int, maxX: int, minY: int, maxY: int,
                 rangeCalculator: rangeCalculator) -> None:
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.width = width
        self.range = rangeCalculator.range
        self.rangeCalculator = rangeCalculator
        self.cadeaux: list[cadeau] = []

    def addCadeau(self, cadeau: cadeau) -> any:
        self.cadeaux.append(cadeau)
        return self

    def getPoids(self) -> int:
        return sum([(0 if elem.delivre else elem.poids) for elem in self.cadeaux])

    def getScore(self) -> int:
        return sum([(0 if elem.delivre else elem.score) for elem in self.cadeaux])

    def getGroups(self) -> list[list[groupe]]:

        # on crées les groupes vides
        ret = []
        for x in range(self.width):
            row = []
            for y in range(self.width):
                row.append(groupe(x, y))
            ret.append(row)

        # on associes les cadeaux aux groupes
        for cadeau in self.cadeaux:
            for i in range(cadeau.positionX - self.range, cadeau.positionX + self.range):
                for j in range(cadeau.positionY - self.range, cadeau.positionY + self.range):
                    if (
                            i - self.minX >= 0 and i - self.minX < self.range and j - self.minY >= 0 and j - self.minY < self.range):
                        if (self.rangeCalculator.isInRange(cadeau.positionX, cadeau.positionY, i, j)):
                            ret[i - self.minX][j - self.minY].addCadeau(cadeau)

        return ret


class heatMap():
    def __init__(self, reachRange: int, cadeaux: list[cadeau]) -> None:
        self.regions: list[list[region]] = []
        self.range = reachRange
        self.rangeCalculator = rangeCalculator(reachRange)
        self.regionSize = 100  # TODO: a fine tune, taille en cases d'un bloc "région"

        # on détecte les limites
        minX = math.inf
        minY = math.inf
        maxX = -math.inf
        maxY = -math.inf
        for cadeau in cadeaux:
            minX = cadeau.positionX if cadeau.positionX < minX else minX
            minY = cadeau.positionY if cadeau.positionY < minY else minY
            maxX = cadeau.positionX if cadeau.positionX > maxX else maxX
            maxY = cadeau.positionY if cadeau.positionY > maxY else maxY

        width = maxX - minX
        height = maxY - minY

        self.offsetX = minX
        self.offsetY = minY

        # on crées les régions en accordance
        for i in range(width // self.regionSize + 1):
            row = []
            for j in range(height // self.regionSize + 1):
                newMinX = minX + i * self.regionSize
                newMinY = minY + j * self.regionSize
                row.append(
                    region(self.regionSize, newMinX, newMinX + self.regionSize, newMinY, newMinY + self.regionSize,
                           self.rangeCalculator))
            self.regions.append(row)

        # on y ajoutes les cadeaux
        for cadeau in cadeaux:
            self.regions[(cadeau.positionX - self.offsetX) // self.regionSize][
                (cadeau.positionY - self.offsetY) // self.regionSize].addCadeau(cadeau)


class traineau:
    def __init__(self, reachRange: int, accelerationCalculator: accelerationCalculator) -> None:
        self.positionX = 0
        self.positionY = 0
        self.vitesseX = 0
        self.vitesseY = 0
        self.nbCarottes = 0
        self.cadeaux: list[
            cadeau] = []  # il est impératif de ne jamais modifier directement cette liste (voir traineau.chargerCadeau et traineau.livrerCadeau)
        self.range = reachRange
        self.rangeCalculator = rangeCalculator(reachRange)
        self.accelerationCalculator = accelerationCalculator

    def accelerer(self, quantity: int, direction: Literal["up", "down", "left", "right"]) -> any:
        # TODO : integrer la verification de l'acceleration max par raport au chargement des cadeaux
        if (quantity > self.accelerationCalculator.getMaxAcceleration(self.getPoids())):
            if (quantity < 0):
                if (self.nbCarottes > 0):
                    if (direction == "up"):
                        self.vitesseY += quantity
                    elif (direction == "down"):
                        self.vitesseY += -quantity
                    elif (direction == "left"):
                        self.vitesseX += -quantity
                    elif (direction == "right"):
                        self.vitesseX += quantity
                    self.nbCarottes += -1
                else:
                    raise RuntimeWarning("il est impossible d'effectuer une acceleration sans carottes")
            else:
                raise ValueError("il est impossible d'effectuer une acceleration négative")
        else:
            raise ValueError(
                "il est impossible d'effectuer une acceleration au dela des limites imposées par le poids du traineau. Poids actuel : " + str(
                    self.getPoids()) + " Acceleration max : " + str(
                    self.accelerationCalculator.getMaxAcceleration(self.getPoids())))
        return self

    def flotter(self, duration: int) -> any:
        for i in range(duration):
            self.positionX += self.vitesseX
            self.positionY += self.vitesseY
        return self

    def chargerCarotte(self, quantity: int) -> any:
        if (self.rangeCalculator.isInRange(self.positionX, self.positionY, 0, 0)):
            if ((self.nbCarottes + quantity) >= 0):
                self.nbCarottes += quantity
            else:
                raise RuntimeWarning("il est impossible d'avoir une quantité négative de carottes'")
        else:
            raise RuntimeWarning("il est impossible de charger des carottes si l'on n'est pas a porté de (0,0)")
        return self

    def chargerCadeau(self, cadeau: cadeau) -> any:
        if (self.rangeCalculator.isInRange(self.positionX, self.positionY, 0, 0)):
            if (cadeau not in self.cadeaux):
                self.cadeaux.append(cadeau)
            else:
                raise RuntimeWarning("un meme cadeau ne peut pas etre chargé deux fois dans le traineau")
        else:
            raise RuntimeWarning("il est impossible de charger un cadeau si l'on n'est pas a porté de (0,0)")
        return self

    def livrerCadeau(self, cadeau: cadeau) -> any:
        if (self.rangeCalculator.isInRange(self.positionX, self.positionY, cadeau.positionX, cadeau.positionY)):
            if (cadeau in self.cadeaux):
                self.cadeaux.remove(cadeau)
                cadeau.delivre = True
            # TODO : implémenter le score
            else:
                raise RuntimeWarning("il est impossible de livrer un cadeau qui n'est pas chargé dans le trainneau")
        else:
            raise RuntimeWarning(
                "il est impossible de charger un cadeau si l'on n'est pas a porté du point de dépot du cadeau")
        return self

    def chargerGroupe(self, groupe: groupe) -> any:
        for cadeau in groupe.cadeaux:
            if (not cadeau.delivre):
                self.chargerCadeau(cadeau)

    def livrerGroupe(self, groupe: groupe) -> any:
        if (self.positionX == groupe.positionX and self.positionY == groupe.positionY):
            for cadeau in groupe.cadeaux:
                if (cadeau in self.cadeaux):
                    self.livrerCadeau(cadeau)
        raise RuntimeWarning("il faut se situer au coordonées exactes du groupe si l'on shouaite le livrer")

    def getPoids(self) -> int:
        return sum([elem.poids for elem in self.cadeaux]) + self.nbCarottes


class chemin:
    def __init__(self, begining: groupe, end: groupe) -> None:
        self.begining = begining
        self.end = end
        self.travelActions: list[list[str | int]] = []

    # format de self.travelActions:
    # [
    # 	["accLeft", 8],
    # 	["float", 3],
    # 	["LoadGift", "Olivia"],
    # 	["DeliverGift", "Bob"],
    # 	["LoadCarrots", 2],
    # 	["LoadGift", "Amine"]
    # ]
    def GetNbActions(self)-> int :
        return len(self.travelActions)

    # TODO : parcours simple - calcul et création des instructions du chemin ici, possibilité d'utilise un objet Traineau

    def __str__(self) -> str:
        chemin_str = str()
        for ligne in self.travelActions :
            ligne[1] = str(ligne[1])
            chemin_str = chemin_str + ' '.join(self.travelActions[ligne]) + '\n'
        return chemin_str


class boucle:
    def __init__(self) -> None:
        self.chemins: list[chemin] = []

    def __str__(self) -> str:
        # TODO : sérialisation - transformation de self.chemins en string ICI
        boucle_str = str()
        for element in self.chemins :
            boucle_str = boucle_str + ' '.join(self.chemins[element]) + '\n'
        return boucle_str


class parcoursFinal:
    def __init__(self) -> None:
        self.boucles: list[boucle] = []

    def __str__(self) -> str:
        # TODO : sérialisation - transformation de self.boucles en string ICI
        parcoursFinal_str = str()
        for element in self.boucles :
            parcoursFinal_str = parcoursFinal_str + ' '.join(self.boucles[element])
        return parcoursFinal_str


filename = "a_an_example.in.txt"

def read(filename: str):
    with open(filename, 'r') as a_fichier:
        contenu = a_fichier.readlines()

    weightsParAccel = list()

    for ligne in contenu:
        if contenu.index(ligne) == 0:
            secondes = int(ligne.split()[0])
            traineau(int(ligne.split()[1]))
            accel_range = int(ligne.split()[2])
            nb_cadeaux = int(ligne.split()[3])

        elif 1 <= contenu.index(ligne) <= accel_range:
            weightsParAccel[contenu.index(ligne) - 1] = [int(ligne.split()[0], int(ligne.split()[1]))]

        elif accel_range < contenu.index(ligne) <= (accel_range + nb_cadeaux):
            cadeau(ligne.split()[0], int(ligne.split()[1]), int(ligne.split()[2]), int(ligne.split()[3]),
                   int(ligne.split()[4]))

    accelerationCalculator(weightsParAccel)
