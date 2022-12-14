from model import traineau, parcoursFinal, boucle, chemin, heatMap,accelerationCalculator

class scorer:
	def __init__(self, parcoursFinal:parcoursFinal, heatMap:heatMap,accelerationCalculator:accelerationCalculator,timeLimit:int) -> None:
		self.map = heatMap
		self.parcoursFinal = parcoursFinal
		self.accelerationCalculator = accelerationCalculator
		self.score = 0
		self.timeLimit = 100

	def compute(self) -> int:
		t = traineau(self.map.range,self.accelerationCalculator)
		instructions = self.parcoursFinal.getInstructions()
		for instruction in instructions:
			match instruction[0]:
				case "AccUp":
					t.accelerer(instruction[1],"up")
				case "AccDown":
					t.accelerer(instruction[1],"down")
				case "AccLeft":
					t.accelerer(instruction[1],"left")
				case "AccRight":
					t.accelerer(instruction[1],"right")
				case "Float":
					t.flotter(instruction[1])
					self.timeLimit += -instruction[1]
				case "LoadCarrots":
					t.chargerCarotte(instruction[1])
				case "LoadGift":
					t.chargerCadeau(self.map.cadeaux.get(instruction[1],None))
				case "DeliverGift":
					t.livrerCadeau(self.map.cadeaux.get(instruction[1],None))
					self.score += self.map.cadeaux.get(instruction[1],None).score
			if(self.timeLimit < 0):
				raise RuntimeWarning("Limite de temps dépassée")
		return self.score
