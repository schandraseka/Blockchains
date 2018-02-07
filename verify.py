import json
from doublehash import doublehash
from oracle import query

with open('test.json', 'r') as f:
	d = json.load(f)
	root = d['root']
	candidate = d['candidate']
	index = d['index']

member = False

#########################
## Your code goes here ##
#########################

#Finding the indices that have to queried. Finding the intervals that have to 
#looked up in the merkle tree and getting their index addresses
def find_parents(indices,index, depth, low, high, offset, order):
	if depth == 0:
		return
	# Check if the index is in first half or second half
	if index >= low+(high-low+1)/2:
		#If in first half we need the merkle value of second half and viceversa
		indices.append((depth-1, 2*offset))
		order.append(True)
		#Traverse one level below and do the same for the updated array
		find_parents(indices, index, depth-1, low+(high-low+1)/2,high, 2*offset+1, order) 
	else:
		#If in first half we need the merkle value of second half and viceversa	
		indices.append((depth-1, 2*offset+1))
		order.append(False)
		#Traverse one level below and do the same for the updated array
		find_parents(indices, index, depth-1, low, low+(high-low+1)/2-1, 2*offset, order)

#TA confirmed that the length for all tests will be 8 on piazza 
#because query function can only query 3 vals and it can be used just once	
length = 8
depth = 3

#Index address in merkle tree
indices = []
#To determine how the hashes have to combined. Left-Right and Right-Left are hashed differently
order = []

#Finding all the indexes to be queried
find_parents(indices, index, depth, 0, length-1, 0, order)


vals = list(query(indices[0], indices[1], indices[2]))
#To compare values from leaf all the way upto root
vals.reverse()
order.reverse()

#Finding the hash of the candidate whose membership has to be validated
candidate_hash = doublehash(candidate)


for i,val in enumerate(vals):
	#As mentioned above left and right children have to be hashed separately
	if order[i] == False:
		candidate_hash = doublehash((candidate_hash<<256) +val)
	else:
		candidate_hash = doublehash((val<<256) +candidate_hash)

if candidate_hash == root:
	member = True

print("Validation Complete. Result : ",member)
#Now indices will contain the has of all the elements that has to be compared at each level
#Iterate it from reverse to get from leaves



with open('test_result.json', 'w') as f:
	f.write(json.dumps(member))


