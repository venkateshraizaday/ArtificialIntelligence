""" This problem has a state space that is taken from an input file given by the user.
For every state we have 16 possible moves. 4 Horizontal moves from in right anf 4 horizontal movrs in left
We can have 4 vertical moves upwards and 4 vertical moves downwards. Thus accounting for 16 moves
We have function that perform these move.

The heuristic funtion is a funtion that calculates manhattan distance for each element in the list and then checks if it is greater than 4. 
If it is greater than 4, it takes 1 moves for all multiples of 4 and add modulus 4 to it then.
Finally we sum up all these distances and arrange list in a priority queue.
We only visit a state once and store all visited states.
"""

""" The cost of visiting a node is its heuristic cost plus the number of moves we needed
 to get to that position. We have assumed our edge cost as 1"""
""" The search algorthim expands nodes in a pririty queue based on the cost. Once a node has been expanded we store it in 
visited, a dictionary here. We expand only unvisited nodes if they are not a solution"""

""" Difficulties faced in computing heuristics and understanding if it is admissible. Further problems in representing data in list 
and storing visited states."""

# The heuristic funtion chosen is calculatiing manhattan distance and then modulating it by 4 
#and adding it to the quotient of manhattan distance  divided by 4.
# It is admissible because we find that whenever the manhattan distance exceeds by 3 
# it takes distance/4 + distance%4 moves to reach the state.
# Example for some scenario we have distance=4, 
# then in our given state space it takes only 1 step to reach the state

#!/usr/bin/python
import sys
from sys import argv
list_dict={}
solution=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
list1=[] # To store current position of 16 puzzle
dist_man=[] # To store Manhattan distance of all current position
visited={}
# Class node to store list, its paths and the cost of reaching it.
class node:
    def __init__(self,list1,cost=0,path="", path1=""):
        self.list1=list1
        self.cost=cost
        self.path=path
        self.path1=path1
        
# Implementation of Priority Queue                
class PriorityQueue:
    def __init__(self):
        self.items=[]
    def isEmpty(self):
        return self.items==[]
    def insert_Node(self,node1):
        return self.items.append(node1)
    def pop_Node(self):
        self.items.sort(key=lambda state:state.cost, reverse=True)
        # Returns based on sorted order of cost
        return self.items.pop()

# Conversion of String to make a dictionary to store visited nodes
def makeString(list1):
    string1=""
    for x in list1:
        string1=string1+x+","
    return string1


def mandist(list1,count,path,path1):
    list=[]
    dist_man=[]
    for ele in list1:
        list.append(ele)
    sum=0
    for x in list:
        index1=list.index(x)
        if x==index1+1:
            dist_man.append(0)
        else:   
            index2=solution.index(x)
            distance=abs(index2-index1)
            if distance>=4:
                distance=distance -3
                if distance>=4:
                    distance=distance-3
                    if distance>=4:
                        distance=distance-3
            distance=distance/4 + distance%4
            dist_man.append(distance)
    for x in dist_man:
        sum+=x
    sum=sum+count
    node1=node(list,sum,path,path1)
    q.insert_Node(node1)
#######################
# Horizonal movement Left
def horizontal(x,list1,count,path,path1):
    list=[]
    for ele in list1:
        list.append(ele)
    a=x/4
    temp=list[a*4+(x)%4]
    list[a*4+(x)%4]=list[a*4+(x+1)%4]
    list[a*4+(x+1)%4]=list[a*4+(x+2)%4]
    list[a*4+(x+2)%4]=list[a*4+(x+3)%4]
    list[a*4+(x+3)%4]=temp
    path=path+ makeString(list1)+ " " +"L" +str(a+1)+ " "
    path1=path1 + "L"+str(a +1) + " " 
    mandist(list,count,path,path1)
    
# Horizonal movement Right
def horizontal_Right(x,list1,count,path,path1):
    list=[]
    for ele in list1:
        list.append(ele)
    a=x/4
    temp=list[a*4+(x)%4]
    list[a*4+(x)%4]=list[a*4+(x-1)%4]
    list[a*4+(x-1)%4]=list[a*4+(x-2)%4]
    list[a*4+(x-2)%4]=list[a*4+(x-3)%4]
    list[a*4+(x-3)%4]=temp
    path=path+ makeString(list1)+ " " +"R" +str(a+1)+ " " 
    path1=path1 + "R"+str(a +1) + " "
    mandist(list,count,path,path1)
    

#######################
# Vertical movement Upwards
def vertical(x,list1,count,path,path1):
    list=[]
    for ele in list1:
        list.append(ele)
    a=x%4
    temp=list[a]
    list[a]=list[a+4]
    list[a+4]=list[a+8]
    list[a+8]=list[a+12]
    list[a+12]=temp
    path=path+ makeString(list1)+ " " +"U" +str(a+1) + " " 
    path1=path1 + "U"+str(a +1) + " "
    mandist(list,count,path,path1) 
# Vertical Movement Downwards
def vertical_Up(x,list1,count,path,path1):
    list=[]
    for ele in list1:
        list.append(ele)
    a=x%4
    temp=list[a+12]
    list[a+12]=list[a+8]
    list[a+8]=list[a+4]
    list[a+4]=list[a]
    list[a]=temp
    path=path + makeString(list1)+ " " +"D" +str(a +1) + " "
    path1=path1 + "D"+str(a +1) + " "
    mandist(list,count,path,path1) 

# To check for all 16 possible movements at a given state
def iteration(count,list1,path,path1):
    x=0
    while x<16:
        prevlist=list1
        horizontal(x,prevlist,count,path,path1)
        horizontal_Right(x, prevlist, count,path,path1)
        x=x+4
    x=0
    while x<4:
        prevlist=list1
        vertical(x,prevlist,count,path,path1)
        vertical_Up(x, prevlist, count, path,path1)
        x=x+1      
#######################
def construct():
# This part of code is for reading input from file and storing it in list
    f = open(str(file),"r")
    line=f.readline()
    while line:
        no=line.split() # To split the read line based on space
        for x in no :
            list1.append(x)
        line = f.readline()
    f.close()
#########################

# Program starts here and runs till queue is not empty
q=PriorityQueue()
file=argv[1]
construct()
node1=node(list1,0,"")
q.insert_Node(node1)
count=0
while not q.isEmpty():
    count=count+1
    node1=q.pop_Node()
    string1=makeString(node1.list1)
    # To check for list if it has already been visited
    if string1 not in visited:
        visited[string1]=True
        if node1.list1==solution:
            node1.path=node1.path+" "+ makeString(solution)
            print "Solution Found Successfully"
            print "Number of Movements required : " + str(count-1)
            print "Path found is : "
            for x in node1.path.split():
                print x
            print "Path Found in terms of directions and row or column number : "
            print node1.path1
            sys.exit()
        else:
            iteration(count,node1.list1,node1.path,node1.path1)

    

    