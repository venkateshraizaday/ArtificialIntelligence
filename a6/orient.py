#from numpy import math
import sys
from sys import argv
import timeit
import math
import random

start = timeit.default_timer()
file = argv[1]
img_train = []
file1 = argv[2]
type = str(argv[3])
if type == "knn":
	k = int(argv[4])

# Distance function to measure similarity. Have used Euclidean distance as a measure of similarity
def distance(x, y):
    dist = 0
    for i in range(2, len(x) - 1):
        dist += pow((x[i] - y[i]), 2)
    return math.sqrt(dist)

# K-nearest neighbors
def knn(test, k):
    dist = []
    # Change range to a smaller number to get results in small time.
    #for x in range(len(img_train) - 1):
    for x in range(100):
        y = distance(test, img_train[x])
        dist.append(y)
    dist_sort = sorted(dist)
    neighbours = []
    for x in range(k):
        neighbours.append(dist.index(dist_sort[x]))
    orientation = [0, 0, 0, 0]
    for x in neighbours:
        if img_train[x][1] == "0":
            orientation[0] += 1
        elif img_train[x][1] == "90":
            orientation[1] += 1
        elif img_train[x][1] == "180":
            orientation[2] += 1
        else:
            orientation[3] += 1
    x = orientation.index(max(orientation))
    if x == 0:
        return "0"
    elif x == 1:
        return "90"
    elif x == 2:
        return "180"
    else:
        return "270"
		
# Helper Functions
def activation_func(value):
	return 1 / (1 + math.exp(-1 * value))
	
def act_diff(x):
	return math.exp(-1*x)/((1 + math.exp(-1*x))**2)
	
def get_output_format(output):
	if output == '0':
		return [1.0,0.0,0.0,0.0]
	elif output == '90':
		return [0.0,1.0,0.0,0.0]
	elif output == '180':
		return [0.0,0.0,1.0,0.0]
	else:
		return [0.0,0.0,0.0,1.0]
		
def returnIndex(num):
	if num == 0:
		return 0
	elif num == 90:
		return 1
	elif num == 180:
		return 2
	else:
		return 3

# Network Design
class neuron:
	def __init__(self,output,delta,input):
		self.output = output
		self.delta = delta
		self.input = input

# To run k-nearest neighbor algorithm
if type == "knn":
    # Learning from training cases    
    f = open(str(file), "r")
    line = f.readline()
    while line:
        # To split the read line based on space
        no = line.split()
        img_train.append(no)
        line = f.readline()
    f.close()
    # Reading and predicting labels for test cases using knn classifier
    for x in range(len(img_train) - 1):
        for y in range(2, len(img_train[x]) - 1):
            img_train[x][y] = int(img_train[x][y])
    
    f1 = open(str(file1), "r")
    line1 = f1.readline();
    fout = open("knn_output.txt", 'w');
    correct = 0
    total = 0
    confusion_mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    while line1:
        # To split the read line based on space
        no = line1.split()
        for i in range(2, len(no) - 1):
            no[i] = int(no[i])   
        x = knn(no, k)
        fout.write(no[0])
        fout.write(" ")
        fout.write(x)
        fout.write("\n")
        total = total + 1
        # To compute confusion matrix
        if int(no[1]) == 0:
            if int(x) == 0:
                confusion_mat[0][0] += 1
            elif int(x) == 90:
                confusion_mat[0][1] += 1
            elif int(x) == 180:
                confusion_mat[0][2] += 1
            else:
                confusion_mat[0][3] += 1
            
        elif int(no[1]) == 90:
            if int(x) == 0:
                confusion_mat[1][0] += 1
            elif int(x) == 90:
                confusion_mat[1][1] += 1
            elif int(x) == 180:
                confusion_mat[1][2] += 1
            else:
                confusion_mat[1][3] += 1
            
        elif int(no[1]) == 180:
            if int(x) == 0:
                confusion_mat[2][0] += 1
            elif int(x) == 90:
                confusion_mat[2][1] += 1
            elif int(x) == 180:
                confusion_mat[2][2] += 1
            else:
                confusion_mat[2][3] += 1
                    
        else:
            if int(x) == 0:
                confusion_mat[3][0] += 1
            elif int(x) == 90:
                confusion_mat[3][1] += 1
            elif int(x) == 180:
                confusion_mat[3][2] += 1
            else:
                confusion_mat[3][3] += 1
        if int(x) == int(no[1]):
            correct += 1  
        line1 = f1.readline()
    f1.close()     
    fout.close()
    # To print Run-time of Algorithm
    stop = timeit.default_timer()
    print "Run-time for the program is " + str(stop - start)
    # Calculation of accuracy for correctly classified images
    accuracy = (correct /float( total))*100
    print "The Classification accuracy of the k-nearest neighbour is " + str(accuracy)
    print correct
    print total
    # To print confusion matrix
    for x in range(4):
        print " "
        for y in range(4):
            sys.stdout.write(str(confusion_mat[x][y]) + " ")

if type == "nnet":
	# Global vars
	input = []
	test_input = []
	output = []
	test_output = []
	alpha = 0.15
	confusion_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

	# Input Layer
	input_layer = []
	input_count = 193

	for iter in range(input_count):
		input_layer.append(neuron(0,0,0))
	input_layer[input_count - 1].output = 1

	# Hidden Layer
	hidden_layer = []
	hidden_count = int(sys.argv[4]) + 1

	for iter in range(hidden_count):
		hidden_layer.append(neuron(0,0,0))
	hidden_layer[hidden_count - 1].output = 1

	# Output Layer
	output_layer = []
	output_count = 4

	for iter in range(output_count):
		output_layer.append(neuron(0,0,0))
		
	# Weight matrices
	w_i_h = []
	w_h_o = []

	for neuron in input_layer:
		temp = []
		for iter in range(hidden_count - 1):
			temp.append(random.random()/10)
		w_i_h.append(temp)
		
	for neuron in hidden_layer:
		temp = []
		for iter in range(output_count):
			temp.append(random.random()/10)
		w_h_o.append(temp)
			
	# Getting input
	fp = open(sys.argv[1],"r")
	line = fp.readline()
	while line:
		data = line.split()
		input.append(data[2:])
		output.append(get_output_format(data[1]))
		line = fp.readline()
		
	# Training network
	for epoch in range(10):
		for iter in range(len(input)):
			for i in range(input_count - 1):
				input_layer[i].output = int(input[iter][i])/100
				
			for i in range(hidden_count - 1):
				z = 0
				for j in range(input_count):
					z += input_layer[j].output * w_i_h[j][i]
				hidden_layer[i].input = z
				hidden_layer[i].output = activation_func(z)
				#print hidden_layer[i].input,hidden_layer[i].output
				
			for i in range(output_count):
				z = 0
				for j in range(hidden_count):
					z += hidden_layer[j].output * w_h_o[j][i]
				output_layer[i].input = z
				output_layer[i].output = activation_func(z)
			
			#print output[iter]
			for i in range(output_count):
				output_layer[i].delta = act_diff(output_layer[i].input) * (output[iter][i] - output_layer[i].output)
				#print output_layer[i].output
				
			for i in range(hidden_count):
				temp = 0
				for j in range(output_count):
					temp += w_h_o[i][j]*output_layer[j].delta
				hidden_layer[i].delta = act_diff(hidden_layer[i].input) * temp
				
			for i in range(input_count):
				for j in range(hidden_count - 1):
					w_i_h[i][j] += alpha * input_layer[i].output * hidden_layer[j].delta
					
			for i in range(hidden_count):
				for j in range(output_count):
					w_h_o[i][j] += alpha * hidden_layer[i].output * output_layer[j].delta
					#print w_h_o[i][j],alpha,hidden_layer[i].output,output_layer[j].delta
				#print " "

	# Getting test input
	fp = open(sys.argv[2],"r")
	line = fp.readline()
	while line:
		data = line.split()
		test_input.append(data[2:])
		test_output.append((data[0],int(data[1])))
		line = fp.readline()
	fp.close()
		
	correct = 0
	total = 0
	fp = open("nnet_output.txt","w")
	for iter in range(len(test_input)):
		for i in range(input_count - 1):
			input_layer[i].output = int(test_input[iter][i])/100
			
		for i in range(hidden_count - 1):
			z = 0
			for j in range(input_count):
				z += input_layer[j].output * w_i_h[j][i]
			hidden_layer[i].input = z
			hidden_layer[i].output = activation_func(z)
			#print hidden_layer[i].input,hidden_layer[i].output
		
		#print test_output[iter]
		result = []
		for i in range(output_count):
			z = 0
			for j in range(hidden_count):
				z += hidden_layer[j].output * w_h_o[j][i]
			output_layer[i].input = z
			output_layer[i].output = activation_func(z)
			result.append(output_layer[i].output)
			#print output_layer[i].output,
		#print " "
		
		actual = returnIndex(test_output[iter][1])
		observed = result.index(max(result))
		if actual == observed:
			correct += 1
		total += 1
		confusion_matrix[actual][observed] += 1
		
		fp.write(test_output[iter][0])
		fp.write(" ")
		if observed == 0:
			fp.write(str(0))
		elif observed == 1:
			fp.write(str(90))
		elif observed == 2:
			fp.write(str(180))
		elif observed == 3:
			fp.write(str(270))
		fp.write("\n")

	print "Percentage: "+str(float(correct)/total*100)
	for i in range(4):
		for j in range(4):
			print confusion_matrix[i][j],
		print ""
	fp.close()
	
if type == "best":
	# Global vars
	input = []
	test_input = []
	output = []
	test_output = []
	alpha = 0.20
	confusion_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

	# Input Layer
	input_layer = []
	input_count = 193

	for iter in range(input_count):
		input_layer.append(neuron(0,0,0))
	input_layer[input_count - 1].output = 1

	# Hidden Layer
	hidden_layer = []
	hidden_count = 49

	for iter in range(hidden_count):
		hidden_layer.append(neuron(0,0,0))
	hidden_layer[hidden_count - 1].output = 1

	# Output Layer
	output_layer = []
	output_count = 4

	for iter in range(output_count):
		output_layer.append(neuron(0,0,0))
		
	# Weight matrices
	w_i_h = []
	w_h_o = []

	for neuron in input_layer:
		temp = []
		for iter in range(hidden_count - 1):
			temp.append(random.random()/10)
		w_i_h.append(temp)
		
	for neuron in hidden_layer:
		temp = []
		for iter in range(output_count):
			temp.append(random.random()/10)
		w_h_o.append(temp)
			
	# Getting input
	fp = open(sys.argv[1],"r")
	line = fp.readline()
	while line:
		data = line.split()
		input.append(data[2:])
		output.append(get_output_format(data[1]))
		line = fp.readline()
		
	# Training network
	for epoch in range(10):
		for iter in range(len(input)):
			for i in range(input_count - 1):
				input_layer[i].output = int(input[iter][i])/100
				
			for i in range(hidden_count - 1):
				z = 0
				for j in range(input_count):
					z += input_layer[j].output * w_i_h[j][i]
				hidden_layer[i].input = z
				hidden_layer[i].output = activation_func(z)
				#print hidden_layer[i].input,hidden_layer[i].output
				
			for i in range(output_count):
				z = 0
				for j in range(hidden_count):
					z += hidden_layer[j].output * w_h_o[j][i]
				output_layer[i].input = z
				output_layer[i].output = activation_func(z)
			
			#print output[iter]
			for i in range(output_count):
				output_layer[i].delta = act_diff(output_layer[i].input) * (output[iter][i] - output_layer[i].output)
				#print output_layer[i].output
				
			for i in range(hidden_count):
				temp = 0
				for j in range(output_count):
					temp += w_h_o[i][j]*output_layer[j].delta
				hidden_layer[i].delta = act_diff(hidden_layer[i].input) * temp
				
			for i in range(input_count):
				for j in range(hidden_count - 1):
					w_i_h[i][j] += alpha * input_layer[i].output * hidden_layer[j].delta
					
			for i in range(hidden_count):
				for j in range(output_count):
					w_h_o[i][j] += alpha * hidden_layer[i].output * output_layer[j].delta
					#print w_h_o[i][j],alpha,hidden_layer[i].output,output_layer[j].delta
				#print " "

	# Getting test input
	fp = open(sys.argv[2],"r")
	line = fp.readline()
	while line:
		data = line.split()
		test_input.append(data[2:])
		test_output.append((data[0],int(data[1])))
		line = fp.readline()
	fp.close()
		
	correct = 0
	total = 0
	fp = open("nnet_output.txt","w")
	for iter in range(len(test_input)):
		for i in range(input_count - 1):
			input_layer[i].output = int(test_input[iter][i])/100
			
		for i in range(hidden_count - 1):
			z = 0
			for j in range(input_count):
				z += input_layer[j].output * w_i_h[j][i]
			hidden_layer[i].input = z
			hidden_layer[i].output = activation_func(z)
			#print hidden_layer[i].input,hidden_layer[i].output
		
		#print test_output[iter]
		result = []
		for i in range(output_count):
			z = 0
			for j in range(hidden_count):
				z += hidden_layer[j].output * w_h_o[j][i]
			output_layer[i].input = z
			output_layer[i].output = activation_func(z)
			result.append(output_layer[i].output)
			#print output_layer[i].output,
		#print " "
		
		actual = returnIndex(test_output[iter][1])
		observed = result.index(max(result))
		if actual == observed:
			correct += 1
		total += 1
		confusion_matrix[actual][observed] += 1
		
		fp.write(test_output[iter][0])
		fp.write(" ")
		if observed == 0:
			fp.write(str(0))
		elif observed == 1:
			fp.write(str(90))
		elif observed == 2:
			fp.write(str(180))
		elif observed == 3:
			fp.write(str(270))
		fp.write("\n")

	print "Percentage: "+str(float(correct)/total*100)
	for i in range(4):
		for j in range(4):
			print confusion_matrix[i][j],
		print ""
	fp.close()