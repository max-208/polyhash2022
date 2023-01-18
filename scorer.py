from model import traineau,heatMap
import fileParser

def score(problemFineName, solutionFileName) -> int:
	(cadeaux, timeLimit,reachrange,acccalc) = fileParser.parseChallenge(problemFineName)
	instructions = fileParser.parseSolution(solutionFileName)
	t = traineau(reachrange,acccalc)
	map = heatMap(reachrange,cadeaux)
	timeSpent = 0
	score = 0
	for instruction in instructions:
		print(t.positionX,t.positionY,t.getPoids(),instruction)
		if instruction[0] == "AccUp":
			t.accelerer(instruction[1],"up")
		elif instruction[0] == "AccDown":
			t.accelerer(instruction[1],"down")
		elif instruction[0] == "AccLeft":
			t.accelerer(instruction[1],"left")
		elif instruction[0] == "AccRight":
			t.accelerer(instruction[1],"right")
		elif instruction[0] == "Float":
			t.flotter(instruction[1])
			timeSpent += instruction[1]
		elif instruction[0] == "LoadCarrots":
			t.chargerCarotte(instruction[1])
		elif instruction[0] == "LoadGift":
			t.chargerCadeau(map.cadeaux.get(instruction[1],None))
		elif instruction[0] == "DeliverGift":
			t.livrerCadeau(map.cadeaux.get(instruction[1],None))
			score += map.cadeaux.get(instruction[1],None).score
		if(timeSpent > timeLimit):
			raise RuntimeWarning("Limite de temps dépassée : ", timeSpent, "/",timeLimit)
	return score
