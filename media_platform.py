import matplotlib.pyplot as plt
import numpy as np
import random
from globals import *
import sys
import time


class MediaPlatform():
	def __init__(self, bias=0.7, verbose=False):
		self.verbose = verbose
		self.num_same = 0
		[self.platform_opinion] = np.random.choice([-1, 1], 1)

		self.bias = bias
		if self.bias > 0:
			self.m = (2 - bias) / (2 * bias)
			self.c = 1 - 2 * self.m

		self.agent_opinions = np.random.uniform(-1, 1, NUM_AGENTS)
		self.t_agent_opinion = self.agent_opinions.copy()
		self.prev_opinions = self.agent_opinions.copy()

	
	def change_agent_opinions(self, posts):
		diff = np.abs(posts - self.agent_opinions)
		strengthen_probs = np.zeros(NUM_AGENTS)
		
		fun1 = diff <= 2 - self.bias
		fun2 = diff > 2 - self.bias

		strengthen_probs[fun1] = 1 - diff[fun1] / 2
		strengthen_probs[fun2] = self.m * diff[fun2] + self.c

		strengthened = np.random.random(NUM_AGENTS) < strengthen_probs
		self.agent_opinions[strengthened] += np.sign(self.agent_opinions[strengthened]) * D			# strengthen opinions
		self.agent_opinions[~strengthened] -= np.sign(self.agent_opinions[~strengthened]) * D		# weaken opinions
		self.agent_opinions = np.clip(self.agent_opinions, -1, 1)
		
		
	def serve_posts(self):
		ctc = np.zeros((NUM_POSTERS, NUM_AGENTS))  # creator to consumer matrix
		ctc = ctc + np.reshape(self.posts, (NUM_POSTERS, 1))
             
		# calculate similarity between creator and consumer opinions
		ctc_consumer_sim = 2 - np.abs(ctc - self.agent_opinions) + sys.float_info.epsilon
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
		self.posts = self.agent_opinions[:NUM_POSTERS] 								# posts are the opinions of the posting agents
		self.posts += np.random.normal(scale=POST_NOISE, size=self.posts.shape) 	# add noise to posts
		self.posts = np.clip(self.posts, -1, 1) 									# clip posts to [-1, 1]

		if PLATFORM_BIAS or RECOMMENDATION_BIAS:
			ctc = self.serve_posts()
			tiled_posts = np.tile(self.posts, (NUM_AGENTS, 1))
			sort_order = np.argsort(ctc.T, axis=1)[:, ::-1]
			tiled_posts = np.take_along_axis(tiled_posts, sort_order, axis=1)

			for i in range(POSTS_PER_DAY):
				selected_posts = tiled_posts[:, i]
				self.change_agent_opinions(selected_posts)
		else:
			selected_posts = np.random.choice(self.posts, POSTS_PER_DAY)
			for i in range(POSTS_PER_DAY):
				posts_i = np.tile(selected_posts[i], NUM_AGENTS)
				self.change_agent_opinions(posts_i)
		
		self.t_agent_opinion = np.vstack((self.t_agent_opinion, self.agent_opinions))

	
	def converged(self):
		'''
		Return True if no opinions have changed in the last CONVERGENCE_NUM time steps
		'''
		if np.all(self.agent_opinions == self.prev_opinions):
			self.num_same += 1
		else:
			self.prev_opinions = self.agent_opinions.copy()
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
		pos = np.sum(self.agent_opinions > 0) / NUM_AGENTS
		neg = np.sum(self.agent_opinions < 0) / NUM_AGENTS

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
		for i in range(NUM_AGENTS):
			ax.plot(self.t_agent_opinion[:, i], label=i)
		

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