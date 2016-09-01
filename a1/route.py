''' 
- Program Description:-
Data is read from the file and is stored in the following dictionaries:-
dict_city_data : Contains distance, time and highway between a pair of cities. key - name of both cities
dict_city : Contains list of cities which have a route from a particular city. Key - name of city
dict_city_lat_long : Contains latitude and longitude of a city. key - name of city.

Based on user input one of the algorithms(bfs,dfs or A*) and rounting option(segment, distance, time) are chosen.
If result is found it is displayed as mentioned in the problem and if not then "No suitable route" is printed.

- Algorithm:-
A node is extracted from the data structure(DFS: Stack, BFS: Queue, A*: Priority Queue) and is checked for being destination node.
If Yes then the route is printed and program exits.
If No then all the cities adjacent to this city are pushed into the data structure.

- Assumptions:-
The input by the user is correct and no spelling mistakes are made.

- Heuristic Function:-
Routing option: Distance
The distance between two cities based on their latitudes and longitudes.
In case the city does not have lat and long, it is assigned the heuristic cost: Heurisitc Cost of parent - distance from parent.

Routing option: Time
The distance between two cities based on their latitudes and longitudes divided by 45.
On looking at the data provided one can see that mean, mode, median(1st quartile, 2nd quartile, 3rd quartile) all have the value ~45 for average speed. Hence the choice.

The function is admissible because the distance is the straight line path between two cities and the answer always be greater than or equal to it.

- Results:-
A* algorithm comes up with the best solution always for all routing option.
BFS comes up with near optimal path most times but not always since edge weights are not one.
DFS rarely comes up with an optimal path.

- Performance:-
Computation time is low for all three algorithms due to use of Dictionaries for data retreival.
Following is the time for each algorithm after being kept in a loop for 1000 times and given the following input:-
"Stafford_Springs,_Connecticut ludlow,_Massachusetts routing_option routing_algo"

    distance time   segment
bfs  224.62  223.91  224.18
dfs  278.81  279.17  278.55
A*   218.22  219.59  217.64

A* is better.
'''

import sys
from math import sin, cos, sqrt,atan2

class new_node():
	def __init__(self, name, time, distance, path, heuristic_cost=0):
		self.name = name
		self.time = time
		self.distance = distance
		self.path = path
		self.heuristic_cost = heuristic_cost

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
		
class Stack:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

class PriorityQueue: 
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		self.items.sort(key=lambda city:city.heuristic_cost, reverse=True)
		return self.items.pop()

q = Queue()
s = Stack()
pq = PriorityQueue()

def construct_data():
	fopen=open("road-segments.txt","r")
	line=fopen.readline()
	while line:
		data=line.split()
		
		i=0
		j=1
		for count in range(2):
			if data[i] in dict_city:
				dict_city[data[i]].append(data[j])
			else:
				dict_city[data[i]] = [data[j]]
			
			distance = float(data[2])
			
			if len(data) == 5:
				if data[3] == '0':
					time = float(data[2])/45
				else:
					time = float(data[2])/float(data[3])
				
				if data[4]:
					highway = data[4]
				else:
					highway = 'No name'
			else:
				time = float(data[2])/45
				highway = data[3]
				
			dict_city_data[data[i]+data[j]] = [distance, time, highway]
			i=1
			j=0

		line = fopen.readline()
	fopen.close()
	
	fopen=open("city-gps.txt","r")
	line=fopen.readline()
	while line:
		data=line.split()
		dict_city_lat_long[data[0]] = [data[1],data[2]]
		line = fopen.readline()
	fopen.close()

def breadth_first_search(start, destination):
	start_node = new_node(start, 0, 0, start)
	q.put(start_node)
	while not q.empty():
		current_node = q.get()
		if current_node.name == destination:
			destination_reached(current_node)
		
		if current_node.name not in visited:
			visited.append(current_node.name)
			#print (visited)
			add_children_BFS(current_node)
	
	print 'No suitable route found'

def add_children_BFS(node):
	children = dict_city[node.name]
	#print (node.name,node.cost,children)
	for child in children:
		name = child
		path = str(node.path) + ' ' + str(child)
		row = dict_city_data[node.name+child]
		time = float(node.time) + row[1]
		distance = float(node.distance) + row[0]
		
		'''if routing_option == 'segment':
			cost = node.cost+1
		elif routing_option == 'distance':
			cost = float(node.cost) + row[0]
		else:
			cost = node.cost + row[1]'''
		q.put(new_node(name, time, distance, path))
		
def depth_first_search(start, destination):
	start_node = new_node(start, 0, 0, start)
	s.push(start_node)
	while not s.isEmpty():
		current_node = s.pop()
		if current_node.name == destination:
			destination_reached(current_node)
		
		if current_node.name not in visited:
			visited.append(current_node.name)
			#print (visited)
			add_children_DFS(current_node)
	
	print 'No suitable route found'

def add_children_DFS(node):
	children = dict_city[node.name]
	#print (node.name,node.cost,children)
	for child in children:
		name = child
		path = str(node.path) + ' ' + str(child)
		row = dict_city_data[node.name+child]
		time = float(node.time) + row[1]
		distance = float(node.distance) + row[0]
		
		s.push(new_node(name, time, distance, path))
		
def a_star_search(start, destination):
	start_node = new_node(start, 0, 0, start, 0)
	pq.push(start_node)
	while not pq.isEmpty():
		current_node = pq.pop()
		if current_node.name == destination:
			destination_reached(current_node)
		
		if current_node.name not in visited:
			visited.append(current_node.name)
			#print (visited)
			add_children_AStar(current_node)
	
	print 'No suitable route found'
	
def add_children_AStar(node):
	children = dict_city[node.name]
	#print (node.name,node.cost,children)
	for child in children:
		name = child
		path = str(node.path) + ' ' + str(child)
		row = dict_city_data[node.name+child]
		time = float(node.time) + row[1]
		distance = float(node.distance) + row[0]
		
		if node.name in dict_city_lat_long:
			curr_city = dict_city_lat_long[node.name]
			lat_curr = float(curr_city[0])
			long_curr = float(curr_city[1])
			dist = distance_lat_long(lat_curr, long_curr, lat_dest, long_dest)
		else:
			dist = node.heuristic_cost - row[0]
		
		if routing_option == 'segment':
			heuristic_cost = int(dist/18) + len(path.split()) - 1
		elif routing_option == 'distance':
			heuristic_cost = dist + distance
		else:
			heuristic_cost = dist/45 + time
		#heuristic_cost = cost + dist
		pq.push(new_node(name, time, distance, path, heuristic_cost))

def distance_lat_long(lat1,long1, lat2,long2):
    r=6371
    dlat= (lat1-lat2)*3.14/180
    dlong=(long1-long2)*3.14/180
    a=sin(dlat/2)**2 + cos(lat1*3.14/180)*cos(lat2*3.14/180)*sin(dlong/2)**2
    c=2*atan2(sqrt(a),sqrt(1-a))
    d=r*c
    return d/1.60934
		
def destination_reached(destination_node):
	#print (visited)
	city_list = destination_node.path.split()
	for i in range(len(city_list)-1):
		temp = dict_city_data[city_list[i]+city_list[i+1]]
		print city_list[i] + ' to ' + city_list[i+1]
		print 'distance: '+str(temp[0])
		print 'time: '+str(temp[1])
		print 'highway: '+temp[2]
		print '\n'
	print destination_node.distance, destination_node.time, destination_node.path
	sys.exit()

#Global Variables
dict_city_data = {}
dict_city = {}
dict_city_lat_long = {}
start = ''
destination = ''
routing_option = ''
routing_algorithm = ''
visited = []

start = sys.argv[1]
destination = sys.argv[2]
routing_option = sys.argv[3]
routing_algorithm = sys.argv[4]

construct_data()

dest_city = dict_city_lat_long[destination]
lat_dest = float(dest_city[0])
long_dest = float(dest_city[1])

if routing_algorithm == 'bfs':
	breadth_first_search(start, destination)
elif routing_algorithm == 'dfs':
	depth_first_search(start, destination)
else:
	a_star_search(start, destination)
