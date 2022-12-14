import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from model import cadeau, heatMap
from random import randint
import time

l = []
hmax = 5000
wmax = 5000
for i in range(10000):
	l.append(cadeau(str(i),1,1,randint(0,wmax),randint(0,hmax)))

t1 = time.perf_counter()
map = heatMap(100,l)
t2 = time.perf_counter()
print(f"Chargement des données {t2 - t1:0.4f} Secondes")
t1 = time.perf_counter()
for i in map.regions:
	for j in i:
		j.getPoids()
t2 = time.perf_counter()
print(f"Recuperation du poids par région {t2 - t1:0.4f} Secondes")
t1 = time.perf_counter()
for k in map.regions[0][0].getGroups():
	for m in k:
		m.getPoids()
t2 = time.perf_counter()
print(f"Chargement du poids de 1 région  {t2 - t1:0.4f} Secondes")
t1 = time.perf_counter()
for i in map.regions:
	for j in i:
		for k in j.getGroups():
			for m in k:
				m.getPoids()
t2 = time.perf_counter()
print(f"Chargement du poids de toute les coordonées  {t2 - t1:0.4f} Secondes")

"""for row in rangeCalculator(3).rangeMask:
	for col in row:
		print("[]" if col else "..",end="")
	print("")
calc = rangeCalculator(3)
print("")
for i in range(7):
	for j in range(7):
		print("[]" if calc.isInRange(3,3,i,j) else "..",end="")
	print("")"""