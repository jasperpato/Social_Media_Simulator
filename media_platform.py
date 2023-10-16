'''
A single instance of a social media simulation

usage:
	python3 media_platform.py
'''

import matplotlib.pyplot as plt
import numpy as np
from globals import *
import sys
import math
import time


class MediaPlatform():
	def __init__(self, b=B, p=P, n=N, c=C, d=D, pb=PB, rb=RB, poster_dist='uniform', verbose=False):
		self.b = b				# agent bias
		self.p = p				# proportion of posting agents
		self.n = n				# standard deviation of Gaussian noise applied to posts
		self.c = c				# proportion of generated posts consumed per day
		self.d = d				# amount opinions are strengthed/weakened by
		self.pb = pb			# platform bias
		self.rb = rb			# recommendation bias
		self.verbose = verbose

		self.num_posters = round(P * NUM_AGENTS)
		self.posts_per_day = round(C * self.num_posters)

		self.num_same = 0
		[self.platform_opinion] = np.random.choice([-1, 1], 1)

		self.m = 0
		self.c = 0

		if self.b > 0:
			self.m = (2 - b) / (2 * b)
			self.c = 1 - 2 * self.m

		self.agent_opinions = np.zeros(NUM_AGENTS)
		if poster_dist == 'uniform':
			self.agent_opinions[:self.num_posters] = np.random.uniform(-1, 1, self.num_posters)
		else:
			opinions = np.linspace(-1, 1, 100)
			if poster_dist == 'bimodal':
				probs = np.cos((opinions + 1) / 2 * np.pi) ** 2
			elif poster_dist == 'centered':
				probs = np.cos(opinions / 2 * np.pi) ** 2
			elif poster_dist == 'skewed':		# skew away from platform opinion
				skew_direction = math.copysign(1, self.platform_opinion)
				probs = np.cos((opinions + skew_direction) / 4 * np.pi) ** 2
			else:
				raise ValueError('Invalid poster distribution')
			probs /= np.sum(probs)
			self.agent_opinions[:self.num_posters] = np.random.choice(opinions, self.num_posters, p=probs)
			
		self.agent_opinions[self.num_posters:] = np.random.uniform(-1, 1, NUM_AGENTS - self.num_posters)
		self.t_agent_opinion = self.agent_opinions.copy()
		self.prev_opinions = self.agent_opinions.copy()
		self.t = 0


	def change_agent_opinions(self, posts):
		diff = np.abs(posts - self.agent_opinions)
		strengthen_probs = np.zeros(NUM_AGENTS)
		
		fun1 = diff <= 2 - self.b
		fun2 = diff > 2 - self.b

		strengthen_probs[fun1] = 1 - diff[fun1] / 2
		strengthen_probs[fun2] = self.m * diff[fun2] + self.c

		strengthened = np.random.random(NUM_AGENTS) < strengthen_probs
		self.agent_opinions[strengthened] += np.sign(self.agent_opinions[strengthened]) * self.d			# strengthen opinions
		self.agent_opinions[~strengthened] -= np.sign(self.agent_opinions[~strengthened]) * self.d			# weaken opinions
		self.agent_opinions = np.clip(self.agent_opinions, -1, 1)
		
		
	def serve_posts(self):
		ctc = np.zeros((self.num_posters, NUM_AGENTS))  # creator to consumer matrix
		ctc = ctc + np.reshape(self.posts, (self.num_posters, 1))
             
		# calculate similarity between creator and consumer opinions
		ctc_consumer_sim = 1 - np.abs(ctc - self.agent_opinions) / 2 + sys.float_info.epsilon
		# calculate similarity between creator and platform opinions
		ctc_platform_sim = 1 - np.abs(ctc - self.platform_opinion) / 2 + sys.float_info.epsilon
            
		ctc = self.pb * ctc_platform_sim + self.rb * ctc_consumer_sim
		ctc = ctc / np.max(ctc, axis=0, keepdims=True)               # normalize with max of each agent's posts
		ctc[np.diag_indices(self.num_posters)] = 0                        # posters should not consume their own posts
		return ctc


	def time_step(self):
		'''
		Each agent consumes its own served posts
		'''
		self.posts = self.agent_opinions[:self.num_posters] 								# posts are the opinions of the posting agents
		self.posts += np.random.normal(scale=self.n, size=self.posts.shape) 	# add noise to posts
		self.posts = np.clip(self.posts, -1, 1) 									# clip posts to [-1, 1]

		if self.pb or self.rb:
			ctc = self.serve_posts()
			tiled_posts = np.tile(self.posts, (NUM_AGENTS, 1))
			sort_order = np.argsort(ctc.T, axis=1)[:, ::-1]
			tiled_posts = np.take_along_axis(tiled_posts, sort_order, axis=1)

			for i in range(self.posts_per_day):
				selected_posts = tiled_posts[:, i]
				self.change_agent_opinions(selected_posts)
		else:
			selected_posts = np.random.choice(self.posts, self.posts_per_day)
			for i in range(self.posts_per_day):
				posts_i = np.tile(selected_posts[i], NUM_AGENTS)
				self.change_agent_opinions(posts_i)
		
		self.t_agent_opinion = np.vstack((self.t_agent_opinion, self.agent_opinions))
		self.t += 1

	
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
		Return the fractions of agents holding positive and negative opinions
		'''
		pos = np.sum(self.agent_opinions > POLARISATION_CUTOFF) / NUM_AGENTS
		neg = np.sum(self.agent_opinions < -POLARISATION_CUTOFF) / NUM_AGENTS

		if self.verbose:
			print(f'Fraction positive {pos}')
			print(f'Fraction negative {neg}')

		return {1: pos, -1: neg}
	

	def polarisation(self):
		'''
		Return polarisation value between [0, 1]
		'''
		return min(self.fractions().values())


	def graph(self):
		'''
		Graph every agent's opinion changing over time
		'''
		_, ax = plt.subplots()
		for i in range(NUM_AGENTS):
			ax.plot(self.t_agent_opinion[:, i], label=i)
		

if __name__ == '__main__':
	start_time = time.time()
	m = MediaPlatform(b=0.6, poster_dist='centered')
	m.simulate()
	print(m.fractions())
	print(m.platform_opinion)
	print(m.t)
	print(f'--- {round(time.time() - start_time, 4)} seconds ---')
	m.graph()
	plt.show(block=True)