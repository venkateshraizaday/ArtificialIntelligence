'''
DESCRIPTION:
The game is based on iterative deepening algorithm.
A best solution is calculated at each level and added to a list.
The top of the solution list is printed when either the execution finishes or the time ends.
The solution list always has the best solution from each iterative level.

- First all the children for the given node are produced.
- if the child is terminal i.e its level is equal to the max_level defined during that iteration then then it is inserted in solution lists.
- else if the evaluation function returns the value zero for the child then it is inserted in the solutions list.
- else children are created for this child and the process is continued from step 2.

Description for each function is given on top of it.
'''

import sys
import time
import threading
import os

# basic structure of the every node.
class new_node():
	def __init__(self,state,level,value,solution):
		self.state = state
		self.level = level
		self.value = value
		self.solution = solution

'''
This function checks if the child is a terminal and then adds it to one of the solution lists
or else it creates its children and calls minimum for all of them.
The win_solution list is for the cases where terminal condition is reached with computer winning.
The lose_solution list is for the cases where terminal condition is reached with computer losing.
'''
def Minimum(node, max_level):
	isTerminal = CheckTerminal(node,max_level)
	KO = GameOver(node)
	value = EvalFunction(node)
	if KO:
		node.value = value
		if node.level % 2 == 1:
			win_solution.append(node)
		else:
			lose_solution.append(node)
	elif value == 0 or isTerminal:
		node.value = value
		if node.level % 2 == 0:
			win_solution.append(node)
		else:
			lose_solution.append(node)
	else:
		children = GetChildren(node)
		for child in children:
			Minimum(child, max_level)
			
#This function sends all the possible children for a given node.
def GetChildren(node):
	children = []
	for i in range(len(node.state)):
		new_string = ''
		if node.state[i] == '.':
			new_string = node.state[:i] + "x" + node.state[i+1:]
			if node.level == 1:
				children.append(new_node(new_string,node.level+1,(n**2)+1,new_string))
			else:
				children.append(new_node(new_string,node.level+1,(n**2)+1,node.solution))
	return children

#This function checks if the level of the node has reached to the max_level for that iteration.
def CheckTerminal(node,max_level):
	if node.level == max_level:
		return True
	else:
		return False

# This function checks if a row or column or diagonal has been filled with x's.
def GameOver(node):
	for i in range(n):
		flag1 = 1
		flag2 = 1
		for j in range(n):
			if node.state[(n*i)+j] == 'x':
				flag1 = flag1 * 1
			else:
				flag1 = flag1 * 0
				
			if node.state[i+(n*j)] == 'x':
				flag2 = flag2 * 1
			else:
				flag2 = flag2 * 0

		if flag1 == 1 or flag2 == 1:
			return True
	
	flag1 = 1
	flag2 = 1
	for i in range(n):
		if node.state[(i*n)+i] == 'x':
			flag1 *= 1
		else:
			flag1 *= 0
		
		if node.state[(n-1)*(i+1)] == 'x':
			flag2 *= 1
		else:
			flag2 *= 0
			
	if flag1 == 1 or flag2 == 1:
		return True
	
	return False

# This function sends the number of moves possible after current node. If the function returns 0 then the current move wins the game.
def EvalFunction(node):
	remaining_positions = 0
	children = GetChildren(node)
	for child in children:
		KO = GameOver(child)
		if not KO:
			remaining_positions += 1
	return remaining_positions

#This function keeps the program running for time alloted at run time
def Timer():
	print "I will take my time!!"
	time.sleep(total_time)
	print all_solutions.pop()
	sys._exit(0)

n = int(sys.argv[1])		# number of rows and columns
start = sys.argv[2]			# the initial state of the rameses board
total_time = int(sys.argv[3])	# time given to find a solution in
t = threading.Thread(target = Timer)
t.start()
start_node = new_node(start,1,(n**2)+1,start)
start_children = GetChildren(start_node)
all_solutions = []

''' 
The iterative deepening loop.
After end of each level in the iterative deepning algorithm, 
the all_solution list is appended with the best possible solution and the program after all possible levels are taken into account.

The best possible solution:-
If we have a nodes in win solution then the list is sorted on the basis of least evaluation function value and lowest level.
else the node with highest evaluation function value (so that places to move can be maximized) in lose_solution list is considered.
'''
for new_level in range(2,start.count('.')+1):
	win_solution = []
	lose_solution = []
	for child in start_children:
		Minimum(child, new_level)
	if len(win_solution) > 0:
		win_solution.sort(key=lambda x:(x.value,x.level), reverse=True)
		all_solutions.append(win_solution.pop().solution)
	else:
		lose_solution.sort(key=lambda x:(x.value,x.level))
		all_solutions.append(lose_solution.pop().solution)
print all_solutions.pop()
sys._exit(0)
