'''
The problem has been formulated as a Constraint Satifaction Problem.
A tree is created and each node is considered as an assignment.
Following is the overview of the process:

- Two dictionaries have been used: one to hold the neighbours of a state and another to hold the possible frequencies.
- Two lists are used. One to denote the assignment of a frequency to the states and other to denote the remaining states without assignments.
- Initially the assignment list is empty and pending list has 50 states.

- When CSP runs it selects a state with following properties:-
	- most constrained state i.e the state with least possible frequencies available.
	- most constraining state i.e the state with most neighbours.
- After this an ordering is set to the available freqencies of the above selected state on the basis of least constraining variable.
- For each value in the ordering the following is done:-
	- if the state-value pair satisfies all provious assignments(constraits check) and also doesn't stop further assignments(forward checking), the assignment is accepted.
	- the pair is added to assignment list and the current assignmnet is passed on to the next level.
- Return value:-
	- If all assignments for a state-value pair fail, a backtrack occurs and 0 is returned.
	- If at some stage the pending list becomes empty, the assignment is written to file and 1 is returned.

Problems Faced:-
The only problem was the choice of data model and also the task of maintaining pending and assignment lists especially in the case of a backtrack.

Performance:-
The program runs fast and gives result for the given legacy-constraints-files in 1 second.
A trade off for speed has been made by using forward checking and not arc consistency and hence AC-3 can be used for fewer backtracks.
The current number of backtracks are still 0 for all the cases tried.
'''

import sys

# The CSP algorithm explained in the comments above.
def csp(list_assignment):
	global back_track
	if len(list_pending) == 0:
		write_to_file(list_assignment)
		return 1
	else:
		next = mcv()
		ordering = lcv(next)
		for value in ordering:
			if check_constraints(list_assignment,next,value) == 1 and forward_checking(next,value) == 1:
				list_assignment.append((next,value))
				if csp(list_assignment)==1:
					return 1
				#print "Backtracks"
				back_track = back_track+1
				list_assignment.pop()
		list_pending.append(next)
		return 0
		
# When assignment is complete this function is called to write to "results.txt".
def write_to_file(assignment):
	fopen=open("results.txt","w")
	for item in assignment:
		fopen.write(item[0]+" "+item[1]+"\n")
	fopen.close()
		
# This function returns the most contrained and constraining variable present in the pending list for assignment.
# Most constrained variable is the one with least available freqencies.
# Most constraining variable is the one with maximum neigbours.
# A list is generated on calculating most constrined variable and from this list the most constraining variable is selected.
def mcv():
	temp = []
	temp1 = []
	for state in list_pending:
		temp.append((state,len(dict_state_frequencies[state])))
	temp.sort(key=lambda x:x[1])
	max_constrain = temp[0][1]
	
	for state in temp:
		if state[1] == max_constrain:
			temp1.append((state[0],len(dict_states_neighbours[state[0]])))
	temp1.sort(key=lambda x:x[1])
	return list_pending.pop(list_pending.index(temp1[-1][0]))

# This function returns a list in order of least constraining value.
# The least constraining value is the one which effects least states on being assigned.
def lcv(state):
	temp = []
	temp1 = []
	for value in dict_state_frequencies[state]:
		count = 0
		for neighbour in dict_states_neighbours[state]:
			if value in dict_state_frequencies[neighbour]:
				count += 1
		temp.append((value,count))
	temp.sort(key=lambda x:x[1])
	for value in temp:
		temp1.append(value[0])
	return temp1
		
# This function checks if the current assignment follows the previous assignments.
# 1 is returned if the current assignment is good.
# 0 is returned if a conflict occurs.
def check_constraints(list_assignment,X,v):
	for assignment in list_assignment:
		if X in dict_states_neighbours[assignment[0]] and v == assignment[1]:
			return 0
	return 1

# The forward checking algorithm which makes sure that an assignment does not clear out the possible frequency assignment for a neighbour.
def forward_checking(state,value):
	for neighbour in dict_states_neighbours[state]:
		if value in dict_state_frequencies[neighbour] and len(dict_state_frequencies[neighbour])==1:
			return 0
	for neighbour in dict_states_neighbours[state]:
		if value in dict_state_frequencies[neighbour]:
			dict_state_frequencies[neighbour].pop(dict_state_frequencies[neighbour].index(value))
	return 1

dict_states_neighbours = {} # Contains a list of neigbours for each state
dict_state_frequencies = {} # Contains a list of possible frequencies for each state.
list_pending = []			# List of states that have not been assigned a value yet.
back_track = 0				# Global variable that records the number of backtracks that have occured.

# populating the dictionaries and lists
fopen=open("adjacent-states","r")
line=fopen.readline()
while line:
	data=line.split()
	dict_states_neighbours[data[0]] = []
	dict_state_frequencies[data[0]] = ['A','B','C','D']
	list_pending.append(data[0])
	for count in range(1,len(data)):
		dict_states_neighbours[data[0]].append(data[count])
	line = fopen.readline()
fopen.close()

# Modifying dict_state_frequencies according to legacy-constraints-files.
fopen = open(sys.argv[1],"r")
line=fopen.readline()
while line:
	data=line.split()
	dict_state_frequencies[data[0]] = []
	for i in range(1,len(data)):
		dict_state_frequencies[data[0]].append(data[i])
	line = fopen.readline()
fopen.close()

# Setting CSP into motion.
list_assignment = []
if csp(list_assignment)==1:
	print "Solution written to file!!!"
	print "Number of backtracks: "+str(back_track)
else:
	print "No solution found"
