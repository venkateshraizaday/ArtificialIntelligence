''' 
 - In this problem I have used a brute force approach to solve the puzzle. 
 - I pass the all possible permutations of the names, orders and locations into a vallidator function which checks if the current arrangement 	 passes all the conditions in the question. 
 - If 'no' the state is discarded and next state is evaluated. 
 - If 'yes' the lists are printed and program exits.
 - The data has been modelled as four lists of name ordered location and recieved(order recieved), where an index i of all four lists gives 	you a valid combination.
 - This helped me formulating my valiidator with ease rather than when using a 5x4 matrix.
 - The only problem i faced was generating all the possible outcomes.
 - solution:-
Heather Amplifier North Avenue Elephant
Frank Elephant Orange Drive Doorknob
Jerry Doorknob Maxwell Street Amplifier
Irene Candelabrum Kirkwood Banister
George Banister Lake Avenue Candelabrum
'''

import sys
from itertools import permutations

def list_vallidator(name, ordered, location, recieved):
	for i in range(5):
		if ordered[i] == recieved[i]:
			return False
	
	if recieved[ordered.index("Candelabrum")] != "Banister":
		return False
	
	if ordered[name.index("Irene")] != recieved[ordered.index("Banister")]:
		return False
	
	if recieved[name.index("Frank")] != "Doorknob":
		return False
		
	if ordered[name.index("George")] != recieved[location.index("Kirkwood")]:
		return False
	
	if ordered[location.index("Kirkwood")] != recieved[location.index("Lake Avenue")]:
		return False
	
	if recieved[name.index("Heather")] != ordered[location.index("Orange Drive")]:
		return False
	
	if recieved[name.index("Jerry")] != ordered[name.index("Heather")]:
		return False
		
	if recieved[location.index("North Avenue")] != "Elephant":
		return False
	
	if recieved[ordered.index("Elephant")] != ordered[location.index("Maxwell Street")]:
		return False
	
	if recieved[location.index("Maxwell Street")] != "Amplifier":
		return False
	
	return True

def list_producer(name, ordered, location, recieved):
	the_list = list(permutations(range(5),5))
	for i in range(120):
		for j in range(120):
			for k in range(120):
				ordered_new = [ordered[the_list[i][0]],ordered[the_list[i][1]],ordered[the_list[i][2]],ordered[the_list[i][3]],ordered[the_list[i][4]]]
				location_new = [location[the_list[j][0]],location[the_list[j][1]],location[the_list[j][2]],location[the_list[j][3]],location[the_list[j][4]]]
				recieved_new = [recieved[the_list[k][0]],recieved[the_list[k][1]],recieved[the_list[k][2]],recieved[the_list[k][3]],recieved[the_list[k][4]]]
				
				result = list_vallidator(name, ordered_new, location_new, recieved_new)
				if result==True:
					print "Name Item_Ordered Location Item_Recieved"
					for l in range(5):
						print name[l],ordered_new[l],location_new[l],recieved_new[l]
					sys.exit()

name_main = ["Heather","Frank","Jerry","Irene","George"]
ordered_main = ["Amplifier","Candelabrum","Doorknob","Banister","Elephant"]
location_main = ["Lake Avenue","Kirkwood","North Avenue","Maxwell Street","Orange Drive"]
recieved_main = ["Candelabrum","Banister","Doorknob","Amplifier","Elephant"]

print list_producer(name_main, ordered_main, location_main, recieved_main)
