# Automatic Zacate game player
# B551 Fall 2015
# PUT YOUR NAME AND USER ID HERE!
#
# Based on skeleton code by D. Crandall
#
# PUT YOUR REPORT HERE!
'''
As in the codebase provided, i implemented the first roll and second roll function to return a subset of the rolled dice.
The third roll sends the category that produces the best score for the given final roll.

First_Roll and Second_Roll:-
This function checks for the possibiilty of "pupusa de queso", "pupusa de frijol", "elote", "triple", "cuadruple", "quintupulo" first.
If the condition is satisfied an empty list is returned. 
else all categories are checked for their expected values with current state of dice and a subset is returned based on the highest expected value.

Third_Roll:-
The dice state is checked for each category and appended to the list if the category is fulfilled.
The category with the maximum score is returned.
If no category is found a random category is returned.

Problems Faced:-
On looking at the results a lot of loopholes can be seen as there are separate individual if else cases and condensing them into shorter ones is kinda difficult.

Analysis:-
The program runs well, the average score is always in the range 200 +- 5.
'''
# This is the file you should modify to create your new smart Zacate player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from ZacateState import Dice
from ZacateState import Scorecard
import random

class ZacateAutoPlayer:

	def __init__(self):
		pass  

	# Categories = [ "unos", "doses", "treses", "cuatros", "cincos", "seises", "pupusa de queso", "pupusa de frijol", "elote", "triple", "cuadruple", "quintupulo", "tamal" ]
	def first_roll(self, dice, scorecard):
		return self.check_categories(dice,scorecard)

	def second_roll(self, dice, scorecard):
		return self.check_categories(dice,scorecard)

	def third_roll(self, dice, scorecard):
		result_list = []
		counts = [dice.dice.count(i) for i in range(1,7)]
		
		if "unos" not in scorecard.scorecard:
			score = dice.dice.count(1)*1
			result_list.append(("unos",score))
		if "doses" not in scorecard.scorecard:
			score = dice.dice.count(2)*2
			result_list.append(("doses",score))
		if "treses" not in scorecard.scorecard:
			score = dice.dice.count(3)*3
			result_list.append(("treses",score))
		if "cuatros" not in scorecard.scorecard:
			score = dice.dice.count(4)*4
			result_list.append(("cuatros",score))
		if "cincos" not in scorecard.scorecard:
			score = dice.dice.count(5)*5
			result_list.append(("cincos",score))
		if "seises" not in scorecard.scorecard:
			score = dice.dice.count(6)*6
			result_list.append(("seises",score))
		if "tamal" not in scorecard.scorecard:
			result_list.append(("tamal",sum(dice.dice)))
		if "triple" not in scorecard.scorecard and max(counts) >= 3:
			score = sum(dice.dice)
			result_list.append(("triple",score))
		if "elote" not in scorecard.scorecard and (2 in counts) and (3 in counts):
			result_list.append(("elote",25))
		if "cuadruple" not in scorecard.scorecard and (max(counts) >= 4):
			score = sum(dice.dice)
			result_list.append(("cuadruple",score))
		if "pupusa de frijol" not in scorecard.scorecard and (len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0):
			result_list.append(("pupusa de frijol",30))
		if "pupusa de queso" not in scorecard.scorecard and sorted(dice.dice) == [1,2,3,4,5] or sorted(dice.dice) == [2,3,4,5,6]:
			result_list.append(("pupusa de queso",40))
		if "quintupulo" not in scorecard.scorecard and max(counts) == 5:
			result_list.append(("quintupulo",50))
		
		if result_list != []:
			result_list.sort(key = lambda tup: tup[1])
			return result_list.pop()[0]
		else:
			return random.choice( list(set(Scorecard.Categories) - set(scorecard.scorecard.keys())) )

	def check_categories(self, dice, scorecard):
		counts = [dice.dice.count(i) for i in range(1,7)]
		
		if "quintupulo" not in scorecard.scorecard and max(counts) == 5:
				return []
			
		elif "pupusa de queso" not in scorecard.scorecard and sorted(dice.dice) == [1,2,3,4,5] or sorted(dice.dice) == [2,3,4,5,6]:
			return []
			
		elif "pupusa de frijol" not in scorecard.scorecard and (len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0):
			send_list = []
			for i in range(1,7):
				if dice.dice.count(i) == 2:
					send_list.append(dice.dice.index(i))
					return send_list
			return []
			
		elif "cuadruple" not in scorecard.scorecard and (max(counts) >= 4):
			send_list = []
			for i in range(1,7):
				if dice.dice.count(i) == 1:
					send_list.append(dice.dice.index(i))
					return send_list
			return []
			
		elif "elote" not in scorecard.scorecard and (2 in counts) and (3 in counts):
			return []
			
		elif "triple" not in scorecard.scorecard and max(counts) >= 3:
			for i in range(1,7):
				if dice.dice.count(i) == 3:
					temp = i
					break
				elif dice.dice.count(i) == 4:
					temp = i
					break
				elif dice.dice.count(i) == 5:
					return []
			count = 0
			send_list = []
			for i in dice.dice:
				if i != temp:
					send_list.append(count)
				count += 1
			return send_list			
		else:
			e_list = []
		
			if "unos" not in scorecard.scorecard:
				e_unos = ((1.0/6)**(5 - dice.dice.count(1))) * 5.0
				e_list.append(("unos",e_unos))
			if "doses" not in scorecard.scorecard:
				e_doses = ((1.0/6)**(5 - dice.dice.count(2))) * 10
				e_list.append(("doses",e_doses))
			if "treses" not in scorecard.scorecard:
				e_treses = ((1.0/6)**(5 - dice.dice.count(3))) * 15
				e_list.append(("treses",e_treses))
			if "cuatros" not in scorecard.scorecard:
				e_cuatros = ((1.0/6)**(5 - dice.dice.count(4))) * 20
				e_list.append(("cuatros",e_cuatros))
			if "cincos" not in scorecard.scorecard:
				e_cincos = ((1.0/6)**(5 - dice.dice.count(5))) * 25
				e_list.append(("cincos",e_cincos))
			if "seises" not in scorecard.scorecard:
				e_seises = ((1.0/6)**(5 - dice.dice.count(6))) * 30
				e_list.append(("seises",e_seises))
			if "tamal" not in scorecard.scorecard:
				e_tamal = ((1.0/2)**(5 - (dice.dice.count(4)+dice.dice.count(5)+dice.dice.count(6)))) * 25
				e_list.append(("tamal",e_tamal))
			
			if e_list != []:
				e_list.sort(key = lambda tup: tup[1])
				return self.roll_dice_subset(e_list,dice,scorecard)
			else:
				return dice.dice

	def roll_dice_subset(self,e_list,dice,scorecard):
		send_list = []
		category = e_list.pop()[0]
		if category == "unos":
			for i in range(5):
				if dice.dice[i] != 1:
					send_list.append(i)
		if category == "doses":
			for i in range(5):
				if dice.dice[i] != 2:
					send_list.append(i)
		if category == "treses":
			for i in range(5):
				if dice.dice[i] != 3:
					send_list.append(i)
		if category == "cuatros":
			for i in range(5):
				if dice.dice[i] != 4:
					send_list.append(i)
		if category == "cincos":
			for i in range(5):
				if dice.dice[i] != 5:
					send_list.append(i)
		if category == "seises":
			for i in range(5):
				if dice.dice[i] != 6:
					send_list.append(i)
		if category == "tamal":
			if sum(dice.dice) < 18:
				return self.roll_dice_subset(e_list,dice,scorecard)
			else:
				for i in range(5):
					if dice.dice[i] != 4 or dice.dice[i] != 5 or dice.dice[i] != 6:
						send_list.append(i)
		return send_list