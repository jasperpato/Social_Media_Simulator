from agent import Agent

import time
import matplotlib.pyplot as plt
import numpy as np
import random
from globals import *
import sys


class MediaPlatform():
	def __init__(self, bias=0.7, verbose=False):
		self.verbose = verbose
		self.agents = [Agent(bias, i < NUM_POSTERS) for i in range(NUM_AGENTS)]
		self.prev_opinions = [a.opinion for a in self.agents]
		self.num_same = 0
		[self.platform_opinion] = np.random.choice([-1, 1], 1)
		
		
	def serve_posts(self):
		ctc = np.zeros((NUM_POSTERS, NUM_AGENTS))  # creator to consumer matrix
		ctc = ctc + np.reshape(self.posts, (NUM_POSTERS, 1))
             
		# calculate similarity between creator and consumer opinions
		ctc_consumer_sim = 2 - np.abs(ctc - self.prev_opinions) + sys.float_info.epsilon
		# calculate similarity between creator and platform opinions
		ctc_platform_sim = 2 - np.abs(ctc - self.platform_opinion) + sys.float_info.epsilon
            
		ctc = PLATFORM_BIAS * ctc_platform_sim + RECOMMENDATION_BIAS * ctc_consumer_sim
		ctc = ctc / np.max(ctc, axis=0, keepdims=True)               # normalize with max of each agent's posts
		ctc[np.diag_indices(NUM_POSTERS)] = 0                        # posters should not consume their own posts
		return ctc


	def time_step(self):
		'''
		Each agent consumes its own served posts
		'''
		self.posts = np.array([a.opinion for a in self.agents[:NUM_POSTERS]], dtype=float)
		self.posts += np.random.normal(scale=POST_NOISE, size=self.posts.shape) 	# add noise to posts
		self.posts = np.clip(self.posts, -1, 1) 									# clip posts to [-1, 1]

		if PLATFORM_BIAS or RECOMMENDATION_BIAS:
			ctc = self.serve_posts()
			for i in range(NUM_AGENTS):
				post_scores = ctc[:, i]
				selected_posts = self.posts[np.argsort(post_scores)][::-1][:POSTS_PER_DAY]
				
				for p in selected_posts:
					self.agents[i].consume_post(p)
				
				self.agents[i].opinions.append(self.agents[i].opinion)
		else:
			selected_posts = np.random.choice(self.posts, POSTS_PER_DAY)
			for a in self.agents:
				for p in selected_posts:
					a.consume_post(p)
				a.opinions.append(a.opinion)

	
	def converged(self):
		'''
		Return True if no opinions have changed in the last CONVERGENCE_NUM time steps
		'''
		opinions = [a.opinion for a in self.agents]
		if opinions[NUM_POSTERS:] == self.prev_opinions[NUM_POSTERS:]:
			self.num_same += 1
		else:
			self.prev_opinions = opinions
			self.num_same = 0

		return self.num_same == CONVERGENCE_NUM


	def simulate(self):
		'''
		Execute the specified time steps, or until convergence of opinions
		'''
		for i in range(NUM_TIME_STEPS):
			if self.verbose:
				print(f'Time step {i}')
			self.time_step()
			if self.converged():
				return


	def fractions(self):
		'''
		Return the fractions of agents holding the extreme opinions [-1, 1]
		'''
		pos = len([a for a in self.agents if a.opinion >= 0]) / NUM_AGENTS
		neg = len([a for a in self.agents if a.opinion < 0]) / NUM_AGENTS

		if self.verbose:
			print(f'Fraction positive {pos}')
			print(f'Fraction negative {neg}')

		return [pos, neg]
	

	def polarisation(self):
		'''
		Return polarisation value between [0, 1]
		'''
		return min(self.fractions())


	def graph(self):
		'''
		Graph every agent's opinion changing over time
		'''
		_, ax = plt.subplots()
		for i, a in enumerate(self.agents):
			ax.plot(a.opinions, label=str(i))
		

if __name__ == '__main__':
	if __name__ == '__main__':
		start_time = time.time()
		np.random.seed(10)
		m = MediaPlatform(bias=0.7)
		m.simulate()
		print(m.fractions())
		print(m.platform_opinion)
		print("--- %s seconds ---" % (time.time() - start_time))
		m.graph()
		plt.show(block=True)