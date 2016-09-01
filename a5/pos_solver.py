###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids:
# Venkatesh Raizaday: vraizada
# Arpit Khandelwal: arkhande
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####
'''
1. How code works:-
(a) Naive bayes: Simply selects the POS tag for a word that has maximum probability of working and if the word is unseen then select 'noun' (Works pretty good surprisingy!!!)
(b) Sampler : First we calculate the posterior distribution for every word in the sentence. Then we create a list having values according to the distribution. Then we have 3000 iterations of seleting a pos tag randomly from the generated list. We throw the first 2000 instances.
(c) Max Marginal: From the last 1000 samples taken from Gibbs sampling, we simply choose the pos tag that occured maximum for each word.
(d) MAP : The posterior probability is calculated using the dynamic programming approch. For any word, probability is the product of (1)transition probibility (2)probability of the word given pos tag (3)posterior probability of previous word. From these probabilities, maximum probibility is selected along with the part of speech tag.
(e) Best : I have chosen the Max Marginal inference as the best algorithm because Gibbs gives a model really close to the actual distribution and hence this is very effective.

2. Result Evaluation:-
		ALGORITHM		Words Correct     Sentences Correct
		  1. Naive:       93.86%               47.73%
        2. Sampler:       90.02%               32.00%
   3. Max marginal:       92.46%               41.00%
            4. MAP:       91.87%               39.79%
           5. Best:       92.46%               41.00%

3. Problems/assumptions/simplifications:-
Probabilities are hard to understand and little tweaks give no significant changes in the performance.

'''

import random
import math

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

	total_words = 0.0
	total_pairs = 0.0
	total_sentences = 0.0
	train_dict_pos = {'adj':0.0,'adv':0.0,'adp':0.0,'conj':0.0,'det':0.0,'noun':0.0,'num':0.0,'pron':0.0,'prt':0.0,'verb':0.0,'x':0.0,'.':0.0}
	train_trans_prob = [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]
	train_dict_words = {}
	train_dict_start = {'adj':0.0,'adv':0.0,'adp':0.0,'conj':0.0,'det':0.0,'noun':0.0,'num':0.0,'pron':0.0,'prt':0.0,'verb':0.0,'x':0.0,'.':0.0}
	MAP_Samples = []
	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling
	def posterior(self, sentence, label):
		ans = 1.0
		for i in range(len(sentence)):
			if sentence[i] in self.train_dict_words:
				temp = self.train_dict_words[sentence[i]][self.returnIndex(label[i])]/sum(self.train_dict_words[sentence[i]]) * self.train_dict_pos[label[i]]
				if temp == 0:
					ans *= 0.00000001
				else:
					ans *= temp
		return math.log(ans)

	# Do the training!
	#
	def train(self, data):
		for row in data:
			self.train_dict_start[row[1][0]] += 1
			self.total_sentences += 1
			for pos in row[1]:
				self.train_dict_pos[pos] += 1
				self.total_words += 1
			for i in range(0,len(row[1])-1):
				self.train_trans_prob[self.returnIndex(row[1][i])][self.returnIndex(row[1][i+1])] += 1
				self.total_pairs += 1
			for i in range(0,len(row[0])):
				if row[0][i] not in self.train_dict_words:
					self.train_dict_words[row[0][i]] = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
				self.train_dict_words[row[0][i]][self.returnIndex(row[1][i])] += 1
		for pos in self.train_dict_pos:
			self.train_dict_pos[pos] = self.train_dict_pos[pos]/self.total_words
		for i in range(12):
			for j in range(12):
				self.train_trans_prob[i][j] = self.train_trans_prob[i][j]/self.total_pairs*10
				
	def returnIndex(self,pos):
		if pos == 'adj':
			return 0
		elif pos == 'adv':
			return 1
		elif pos == 'adp':
			return 2
		elif pos == 'conj':
			return 3
		elif pos == 'det':
			return 4
		elif pos == 'noun':
			return 5
		elif pos == 'num':
			return 6
		elif pos == 'pron':
			return 7
		elif pos == 'prt':
			return 8
		elif pos == 'verb':
			return 9
		elif pos == 'x':
			return 10
		elif pos == '.':
			return 11
	
	def returnPOS(self,index):
		if index == 0:
			return 'adj'
		elif index == 1:
			return 'adv'
		elif index == 2:
			return 'adp'
		elif index == 3:
			return 'conj'
		elif index == 4:
			return 'det'
		elif index == 5:
			return 'noun'
		elif index == 6:
			return 'num'
		elif index == 7:
			return 'pron'
		elif index == 8:
			return 'prt'
		elif index == 9:
			return 'verb'
		elif index == 10:
			return 'x'
		elif index == 11:
			return '.'

	# Functions for each algorithm.
	#
	def naive(self, sentence):
		solution = [[]]
		for word in sentence:
			if word in self.train_dict_words:
				solution[0].append( self.returnPOS( self.train_dict_words[word].index(max(self.train_dict_words[word])) ) )
			else:
				solution[0].append('noun')
		return [ solution, [] ]

	def mcmc(self, sentence, sample_count):
		prob_posterior = []
		for word in sentence:
			temp_list = []
			for i in range(12):
				if word in self.train_dict_words:
					temp = (self.train_dict_words[word][i]/sum(self.train_dict_words[word]))*self.train_dict_pos[self.returnPOS(i)]
				else:
					temp = self.train_dict_pos[self.returnPOS(i)]/12
				temp_list.append(temp)
			prob_posterior.append(temp_list)
			
		SampleList = self.makeSet(prob_posterior)
		MCMC_samples = []
		self.MAP_Samples = []
		for iter in range(3000):
			temp_list = []
			for i in range(len(sentence)):
				temp = random.choice(SampleList[i])
				temp_list.append(temp)
			MCMC_samples.append(temp_list)
		self.MAP_Samples = MCMC_samples[2000:]
		return [ MCMC_samples[2000:2005], [] ]

	def makeSet(self,prob_posterior):
		for prob_list in prob_posterior:
			for i in range(12):
				if prob_list[i] != 0 and prob_list[i] < 1:
					while prob_list[i] < 1:
						for j in range(12):
							prob_list[j] = prob_list[j] * 10
		
		final_list = []
		for prob_list in prob_posterior:
			#print prob_list
			temp_list = (['adj']*int(prob_list[0])+['adv']*int(prob_list[1])+['adp']*int(prob_list[2])+['conj']*int(prob_list[3])+['det']*int(prob_list[4])+['noun']*int(prob_list[5])+['num']*int(prob_list[6])+['pron']*int(prob_list[7])+['prt']*int(prob_list[8])+['verb']*int(prob_list[9])+['x']*int(prob_list[10])+['.']*int(prob_list[11]))
			final_list.append(temp_list)
		return final_list
		
	def best(self, sentence):
		(solution , x ) = self.max_marginal(sentence)
		return [ solution, [] ]

	def max_marginal(self, sentence):
		dict_marginal_dist = {}
		solution = [[]]
		values = [[]]
		len_sentence = len(sentence)
		for word in sentence:
			dict_marginal_dist[word] = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
		for row in self.MAP_Samples:
			for i in range(len_sentence):
				dict_marginal_dist[sentence[i]][self.returnIndex(row[i])] += 1
		for i in range(len_sentence):
			values[0].append(max(dict_marginal_dist[sentence[i]])/1000)
			solution[0].append(self.returnPOS(dict_marginal_dist[sentence[i]].index(max(dict_marginal_dist[sentence[i]]))))
		return [ solution, values ]

	def viterbi(self, sentence):
		prob_posterior = []
		solution = [[]]
		for i in range(len(sentence)):
			if i == 0:
				list_temp = []
				if sentence[i] in self.train_dict_words:
					for j in range(12):
						temp = (self.train_dict_start[self.returnPOS(j)]/self.total_sentences) * self.train_dict_words[sentence[i]][j]/sum(self.train_dict_words[sentence[i]])
						list_temp.append(temp)
				else:
					for j in range(12):
						list_temp.append(self.train_dict_start[self.returnPOS(j)]/self.total_sentences)
				prob_posterior.append((max(list_temp),self.returnPOS(list_temp.index(max(list_temp)))))
			else:
				list_temp = []
				if sentence[i] in self.train_dict_words:
					for j in range(12):
						temp = prob_posterior[i-1][0] * self.train_dict_words[sentence[i]][j]/sum(self.train_dict_words[sentence[i]]) * self.train_trans_prob[self.returnIndex(prob_posterior[i-1][1])][j]
						list_temp.append(temp)
				else:
					for j in range(12):
						temp = prob_posterior[i-1][0] * self.train_trans_prob[self.returnIndex(prob_posterior[i-1][1])][j]
						list_temp.append(temp)
				prob_posterior.append((max(list_temp),self.returnPOS(list_temp.index(max(list_temp)))))
		for i in range(len(sentence)):
			solution[0].append(prob_posterior[i][1])
		return [ solution, [] ]


	# This solve() method is called by label.py, so you should keep the interface the
	#  same, but you can change the code itself. 
	# It's supposed to return a list with two elements:
	#
	#  - The first element is a list of part-of-speech labelings of the sentence.
	#    Each of these is a list, one part of speech per word of the sentence.
	#    Most algorithms only return a single labeling per sentence, except for the
	#    mcmc sampler which is supposed to return 5.
	#
	#  - The second element is a list of probabilities, one per word. This is
	#    only needed for max_marginal() and is the marginal probabilities for each word.
	#
	def solve(self, algo, sentence):
		if algo == "Naive":
			return self.naive(sentence)
		elif algo == "Sampler":
			return self.mcmc(sentence, 5)
		elif algo == "Max marginal":
			return self.max_marginal(sentence)
		elif algo == "MAP":
			return self.viterbi(sentence)
		elif algo == "Best":
			return self.best(sentence)
		else:
			print "Unknown algo!"
