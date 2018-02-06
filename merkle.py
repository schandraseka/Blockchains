# Starter code for assignment 1
import json, math
from doublehash import doublehash

# load the leaves as input
leaves = []
with open('leaves.json', 'r') as f:
	leaves = json.load(f)

merkleTree = []

#########################
## Your code goes here ##
#########################

#Yielding n elements at a time
def slicer(leaves, n):
	for i in range(0, len(leaves), n):
		yield leaves[i:i+n]

#Recursive method
def create_tree(merkleTree,leaves, level, depth):
	#Assuming that each level is a power of 2 except for root
	for i in slicer(leaves, 2):
		#Non leaf nodes
		if level != 0:
			merkleTreeValue = doublehash((i[0]<<256) +i[1])
			merkleTree[level].append(merkleTreeValue)
		#Leaf nodes		
		else:
			merkleTree[level].append(doublehash(i[0]))
			merkleTree[level].append(doublehash(i[1]))
	#Exit condition. Entire tree has been built
	if level == depth:
		return
	#Build next level
	else:
		leaves = merkleTree[level]		
		level+=1
		merkleTree.append([])
		create_tree(merkleTree, leaves, level, depth)
	
#Making the tree 2D as it is supposed to be
merkleTree.append([])
#Depth of the tree
depth = math.log(len(leaves),2)

#Constructing the tree
create_tree(merkleTree, leaves, 0, depth)

print("Construction complete")

# write the tree to a file
with open('tree.json', 'w') as f:
	f.write(json.dumps(merkleTree, indent=2))
