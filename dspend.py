import random
import json

def sim(q,z):
    """fill this in"""
    honest_length = 0
    attacker_length = 0
    while(True):
    	if random.random() <= q:
    		attacker_length += 1
    	else:
    		honest_length += 1
    	if honest_length >= z and attacker_length - honest_length >= 1:
    		return 1
    	if honest_length >= z and honest_length - attacker_length >= 35:
    		return 0


results = [[0.0 for i in range(50)] for j in range(50)]
for q in range(50):
    for z in range(50):
        result = 0
        for _ in range(800):
            result += sim(q*0.01, z+1)
        results[q][z] = result/800

def lookup(q, phi):
    z = -1
    for i in range(50):
        if results[int(q*100)][i] < phi:
            return i+1
    return -1


json_str = open('testds.json','r').read()
tests=json.loads(json_str)

with open('results.csv','w') as fd:
  for test in tests:
    fd.write("q:\t%.2f\tPhi:%f\tz:%2d" % (test['q'],test['phi'],lookup(test['q'],test['phi'])))
    #print(test['q'],test['phi'],get_z(test['q'],test['phi']))



