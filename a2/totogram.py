'''
k:3
Solution: 3
5 2 6 8 1 3 4 7 9 10
Time: 0.0522

k:4
Solution: 4
11 7 12 15 3 4 8 13 18 19 1 2 5 6 9 10 14 16 17 20 21 22
Time: 0.0519

k:5
Solution: 6
23 17 24 29 11 12 18 25 34 35 5 6 7 10 15 20 28 31 37 39 40 41 1 2 3 4 8 9 13 14 16 19 21 22 26 27 30 32 33 36 38 42 43 44 45 46
Time: 0.0533

k:6
Solution: 10
47 37 48 57 27 28 38 49 66 67 17 18 19 22 31 40 56 59 73 75 76 77 7 8 9 10 13 16 23 26 32 35 41 44 52 55 61 64 69 72 79 82 84 85 86 87 1 2 3 4 5 6 11 12 14 15 20 21 24 25 29 30 33 34 36 39 42 43 45 46 50 51 53 54 58 60 62 63 65 68 70 71 74 78 80 81 83 88 89 90 91 92 93 94
Time: 0.0578

k:7
Solution: 16
95 79 96 111 63 64 80 97 126 127 47 48 49 50 65 78 112 113 140 141 142 143 31 32 33 34 35 36 43 54 61 71 81 88 104 114 121 129 137 148 154 155 156 157 158 159 15 16 17 18 19 20 21 22 25 28 37 40 44 51 55 58 62 68 72 75 82 85 89 92 100 103 107 110 117 120 124 130 133 136 144 147 151 160 163 166 168 169 170 171 172 173 174 175 1 2 3 4 5 6 7 8 9 10 11 12 13 14 23 24 26 27 29 30 38 39 41 42 45 46 52 53 56 57 59 60 66 67 69 70 73 74 76 77 83 84 86 87 90 91 93 94 98 99 101 102 105 106 108 109 115 116 118 119 122 123 125 128 131 132 134 135 138 139 145 146 149 150 152 153 161 162 164 165 167 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190
Time: 0.0676

PROGRAM DESCRIPTION:
The program has two parts:-
1. Calculating the solution.
2. Creating the tree with the given solution.

Calclating the solution:-
- The best solution can only be found if the root is middle element.
- Now the leftmost leaf node(1) should be reached from root node in best_solution * depth-1 times i.e 1 <= mid - (best_solution * (depth-1))
- Similarly rightmost leaf node (Number of nodes) >= mid + (best_solution * (depth-1))

Creating the tree:-
- A basic bfs approach can be used to create the tree.

Every function has its whole detailed description.
'''
import sys

# Structure of every node in the 2-3 tree
class new_node():
	def __init__(self,value,level,children = {}):
		self.value = value
		self.level = level
		self.children = {}

# Sample queue structure that will be used in implementation of bfs
class Queue: 
	def __init__(self):
		self.in_stack = []
		self.out_stack = []
	def put(self, obj):
		self.in_stack.append(obj)
	def get(self):
		if not self.out_stack:
			while self.in_stack:
				self.out_stack.append(self.in_stack.pop())
		return self.out_stack.pop()
	def empty(self):
		if len(self.in_stack)+len(self.out_stack) == 0:
			return True
		else:
			return False

# This function calculates the best solution for a given depth.
def best_solution():
	result = 1;
	while 1:
		if (mid - (depth - 1)*result) <= 1:
			flag = 1
		else:
			flag = 0
			
		if (mid + (depth - 1)*result) >= n:
			flag = 1
		else:
			flag = 0
		
		if flag==1:
			return result
		result += 1
		
'''
This function does the following:-
1. Create 3 children for the root node.
2. For middle child it creates the value using mid+1
3. For left child it creates the left child of the left child until depth level is reached.
4. And similarly for the right child.
5. Finally Create remaining tree for left,center and right row.
'''
def Initialize_Game():
	root.children["center"] = new_node(mid + 1, root.level + 1)
	remaining.pop(remaining.index(mid+1))
	
	node_left = root
	node_right = root
	while node_left.level != depth-1:
		node_left.children["left"] = new_node(remaining.pop(remaining.index(mid - solution*node_left.level)), node_left.level+1)
		node_right.children["right"] = new_node(remaining.pop(remaining.index(mid + solution*node_right.level)), node_right.level+1)
		node_left = node_left.children["left"]
		node_right = node_right.children["right"]
		
	node_left.children["left"] = new_node(remaining.pop(remaining.index(1)), depth)
	node_right.children["right"] = new_node(remaining.pop(remaining.index(n)), depth)
	
	Create_Tree(root.children["left"],1)
	Create_Tree(root.children["right"],2)
	Create_Tree(root.children["center"],3)

'''
This level creates the remaining tree.
Flags:-
1 : Request is from left node
Create left and right children for the node and then create tree for left child and then right child with flag = 1.
2 : Request is from right node
Create right and left children for the node and then create tree for right child and then left child with flag = 2.
3 : Request if from center node
Create left and right children for the node and then create left tree with flag =1 and right tree with flag = 2.
'''
def Create_Tree(node,flag):
	if node.level == depth:
		return
	if flag == 1:
		if "left" not in node.children:
			node.children["left"] = new_node(Next_Val(node.value,flag),node.level + 1)
		Create_Tree(node.children["left"],1)
		if "right" not in node.children:
			node.children["right"] = new_node(Next_Val(node.value,flag),node.level + 1)
		Create_Tree(node.children["right"],1)
	if flag == 3:
		if "left" not in node.children:
			node.children["left"] = new_node(Next_Val(node.value,flag),node.level + 1)
		Create_Tree(node.children["left"],1)
		if "right" not in node.children:
			node.children["right"] = new_node(Next_Val(node.value,flag),node.level + 1)
		Create_Tree(node.children["right"],2)
	if flag==2:
		if "right" not in node.children:
			node.children["right"] = new_node(Next_Val(node.value,flag),node.level + 1)
		Create_Tree(node.children["right"],2)
		if "left" not in node.children:
			node.children["left"] = new_node(Next_Val(node.value,flag),node.level + 1)
		Create_Tree(node.children["left"],2)

'''
Sends value to for the next node to be created.
If flag is 1 minimum value available is sent and if flag is 2 maximum available value is sent.
If the difference between parent and child node is greater than solution that then next best candidate is selected from remaining.
The process is continued untill the appropriate solution is calculated.
All the values popped from remaining are inserted back again.
'''
def Next_Val(parent,flag):
	new_list = []
	if flag == 2:
		remaining.sort()
	else:
		remaining.sort(reverse=True)
		
	child = remaining.pop()
	
	if abs(parent - child) <= solution:
		return child
		
	else:
		while abs(parent - child) > solution:
			new_list.append(child)
			child = remaining.pop()
		new_list.sort(reverse = True)
		for i in new_list:
			remaining.append(i)
		return child

'''
Basic implementation of bfs algo which keeps on adding children untill depth is reached
'''
def bfs():
	while not queue_bfs.empty():
		node = queue_bfs.get()
		print node.value,
		if node == root:
			queue_bfs.put(node.children["left"])
			queue_bfs.put(node.children["center"])
			queue_bfs.put(node.children["right"])
		elif node.level < depth:
			queue_bfs.put(node.children["left"])
			queue_bfs.put(node.children["right"])
		
queue_bfs = Queue()				#Creating queue that will be used in the bfs algo
depth = int(sys.argv[1])		#Getting depth from input
n = 3*(2**(depth-1) + -1) + 1	#Calculating total number of nodes
mid = n/2						#Identifying the mid element

remaining = []					#This is the list of numbers sorted in decreasing order that haven't been assigned a node yet.
for value in range(n):
	remaining.append(value + 1)
remaining.sort(reverse=True)

solution = best_solution()		#Calculating the solution
print "Solution: "+ str(solution)

root = new_node(mid,1)			#Building the tree with the calculated solution with mid element as the root node.
remaining.pop(remaining.index(mid))
Initialize_Game()
queue_bfs.put(root)
bfs()