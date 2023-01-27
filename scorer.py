from model import traineau,heatMap,rangeCalculator
import fileParser

def score(problemFineName, solutionFileName) -> int:
	(cadeaux, timeLimit,reachrange,acccalc) = fileParser.parseChallenge(problemFineName)	
	instructions = fileParser.parseSolution(solutionFileName)
	r = rangeCalculator(reachrange)
	t = traineau(r,acccalc)
	map = heatMap(r,cadeaux)
	timeSpent = 0
	score = 0
	for instruction in instructions:
		print(t.positionX,t.positionY,t.getPoids(),instruction)
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
				timeSpent += instruction[1]
			case "LoadCarrots":
				t.chargerCarotte(instruction[1])
			case "LoadGift":
				t.chargerCadeau(map.cadeaux.get(instruction[1],None))
			case "DeliverGift":
				t.livrerCadeau(map.cadeaux.get(instruction[1],None))
				score += map.cadeaux.get(instruction[1],None).score
		if(timeSpent > timeLimit):
			raise RuntimeWarning("Limite de temps dépassée : ", timeSpent, "/",timeLimit)
	return score
