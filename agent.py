import random
from globals import *

class Agent:
    
	def __init__(self, is_poster):
		self.is_poster = is_poster
		self.opinion = 2 * random.random() - 1
		self.opinions = [self.opinion]

	def prob_strengthen(self, d):
		'''
		Given difference between opinions, return probability of agent's opinion being strengthened
		'''
		if d <= 2 - B:
			return 1 - d/2
		else:
			return M*d + C

	def consume_post(self, opinion):
		'''
		Update agent's opinion given a post
		'''
		if self.opinion == 0:
			if opinion != 0:
				# agent is unbiased, go in the direction of the post
				self.opinion += D if opinion > 0 else -D
		else:
			d = abs(opinion - self.opinion)
			if random.random() < self.prob_strengthen(d):
				# strengthen opinion
				self.opinion += D if self.opinion > 0 else -D
			else:
				# weaken opinion
				self.opinion += -D if self.opinion > 0 else D 
		
		self.opinion = max(-1, self.opinion)
		self.opinion = min(1, self.opinion)

		self.opinions.append(self.opinion)
