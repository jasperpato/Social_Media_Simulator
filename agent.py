import numpy as np
from globals import *

class Agent:
    
	def __init__(self, bias=0, is_poster=False):
		self.bias = bias
		if self.bias > 0:
			self.m = (2 - bias) / (2 * bias)
			self.c = 1 - 2 * self.m

		self.is_poster = is_poster
		self.opinion = 2 * np.random.sample() - 1
		self.opinions = [self.opinion]

	def prob_strengthen(self, d):
		'''
		Given difference between opinions, return probability of agent's opinion being strengthened
		'''
		if d <= 2 - self.bias:
			return 1 - d/2
		else:
			return self.m * d + self.c

	def consume_post(self, opinion):
		'''
		Update agent's opinion given a post
		'''
		# if self.is_poster: return

		if self.opinion == 0:
			if opinion != 0:
				# agent is unbiased, go in the direction of the post
				self.opinion += D if opinion > 0 else -D
		else:
			d = abs(opinion - self.opinion)
			if np.random.random() < self.prob_strengthen(d):
				# strengthen opinion
				self.opinion += D if self.opinion > 0 else -D
			else:
				# weaken opinion
				self.opinion += -D if self.opinion > 0 else D 
		
		self.opinion = max(-1, self.opinion)
		self.opinion = min(1, self.opinion)

		# self.opinions.append(self.opinion)
